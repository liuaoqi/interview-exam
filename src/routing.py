from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
from gridfs import GridFS, GridFSBucket

from bson.objectid import ObjectId
from typing import List
from datetime import datetime, date
import pandas as pd
from json import loads, dumps

from models import Payee, Filter, PaymentUpdate

router = APIRouter()

# Get payments based on filter/search options
@router.get("/", response_description="List all payments", response_model=List[Payee])
async def get_payments(request: Request, filter: Filter = None, skip: int = 0, limit: int = 100):
    '''
    Fetches payments with the following calculations performed server-side:
    Change the payee_payment_status to "due_now" if payee_due_date is today.
    Change the payee_payment_status to "overdue" if payee_due_date is smaller than today.
    Calculate total_due based on discount, tax and due_amount,
    should support filter, search and pagination

    Includ filter, search and paging options in request body
    '''
    payees = []
    # TODO:
    if filter:
        first_name = filter.first_name
    try:
        payees = list(request.app.database["payments"].find().skip(skip).limit(limit))
        df = pd.DataFrame(payees)
    
        # Change the payment status based on the date
        def update_status(row):
            if row["status"] != "completed":
                if datetime.strptime(row["due_date"], "%Y-%m-%d").date() < date.today():
                    row["status"] = "overdue"
                elif datetime.strptime(row["due_date"], "%Y-%m-%d").date() == date.today():
                    row["status"] = "due_now"
            return row

        df = df.apply(update_status, axis=1)

        # Calculate total_due based on discount, tax and due_amount
        def calculate_amount(row):
            payment = row["payment"]
            if payment:
                discount = payment.get("discount_percent")
                due_amount = payment.get("due_amount")
                tax_percent = payment.get("tax_percent")
                total_due = due_amount*(1-discount*0.01)*(1+tax_percent*0.01)
                return round(total_due, 2)
            return -1

        df["total_due"] = df.apply(calculate_amount, axis=1)
        print(df)
        payees = loads(df.to_json(orient='records'))
        print(payees)

    except Exception as e:
        print(e)

    return payees

# Create a new payment
@router.post("/", response_description="Create a new payment", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_payment(request: Request, payment: Payee = Body(...)):
    '''
    Creates a new payment. Returns the ID of the new record or error.
    '''
    # Create a new payment for the current user with a payment id
    created_payment = ""
    try:
        payment = jsonable_encoder(payment)
        new_payment = request.app.database["payments"].insert_one(payment)
        created_payment = str(new_payment.inserted_id)
    except Exception as e:
        print(e)

    return created_payment

# Update a payment
@router.put("/{id}", response_description="Update a payment", response_model=Payee)
async def update_payment(id: str, request: Request, payment_update: PaymentUpdate = Body(...)):
    '''
    Updates one payment.
    '''
    id = ObjectId(id)

    # Validate the given id
    payment = request.app.database["payments"].find_one({"_id": id})
    
    if payment:
        update = {}
        # Update due amount
        if payment_update.amount:
            due_amount = payment["payment"]["due_amount"] - payment_update.amount
            update["payment"] = payment["payment"]
            update["payment"]["due_amount"] = round(due_amount, 2)

        # Update the status corresponding to time
        if datetime.strptime(payment["due_date"], "%Y-%m-%d").date() < date.today():
            update["status"] = "overdue"
        elif datetime.strptime(payment["due_date"], "%Y-%m-%d").date() == date.today():
            update["status"] = "due_now"

        try:
            request.app.database["payments"].update_one({"_id": id}, {"$set": update})
        except Exception as e:
            print(e)

        # Returns the updated payment
        updated = request.app.database["payments"].find_one({"_id": id})

        return updated

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment not found")

# Delete a payment
@router.delete("/{id}", response_description="Delete a payment")
async def delete_payment(id: str, request: Request, response: Response):
    '''
    Deletes one payment by ID. Returns success or error.
    '''
    id = ObjectId(id)
    delete_result = request.app.database["payments"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment with ID {id} not found")


FILE_TYPES = ["application/pdf", "image/png", "image/jpeg"]

# Upload an evidence file
@router.post("/evidence/{id}", response_description="Upload evidence file for a payment")
async def upload_evidence(id: str, request: Request, file: UploadFile = File(...)):
    '''
    Allows uploading evidence files (PDF, PNG, JPG) when updating status to completed.
    '''
    id = ObjectId(id)
    payment = request.app.database["payments"].find_one({"_id": id})
    # Validate the given id
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    # if payment["status"] != "completed":
    #     raise HTTPException(status_code=400, detail="Payment status must be 'completed' to upload evidence.")
    
    fs = GridFS(request.app.database)
    
    # Validate the file type
    if file.content_type not in FILE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF, PNG, and JPG are allowed.")

    # Upload the file
    file_id = fs.put(await file.read(), filename=file.filename, content_type=file.content_type)
    request.app.database["payments"].update_one({"_id": id}, {"$set": {"evidence_file_id": file_id}})

    # Mark payment as completed when an evidence is uploaded
    if payment["payment"]["due_amount"] == 0:
        request.app.database["payments"].update_one({"_id": id}, {"$set": {"status": "completed"}})

    return {"message": "Evidence file uploaded successfully"}

# Download an evidence file
@router.get("/evidence/download/{id}", response_description="Download evidence file for a payment")
async def download_evidence(id: str, request: Request):
    '''
    Returns uploaded evidence file which should be save from UI.
    '''
    id = ObjectId(id)
    payment = request.app.database["payments"].find_one({"_id": id})
    # Validate the payment id
    if not payment or "evidence_file_id" not in payment:
        raise HTTPException(status_code=404, detail="Evidence file not found")

    fs = GridFS(request.app.database)

    file_id = payment["evidence_file_id"]
    file_id = ObjectId(file_id)
    
    # Get the evidence file from database
    file = fs.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Evidence file not found")
    file_data = file.read()

    # If file_data is None or empty, return an error
    if not file_data:
        raise HTTPException(status_code=404, detail="Evidence file content not found")

    # Create a BytesIO stream from the file content
    file_stream = BytesIO(file_data)

    # Set the appropriate headers for downloading
    headers = {"Content-Disposition": f"attachment; filename={payment['first_name']}_evidence.pdf"}

    # Return the file stream as a response
    return StreamingResponse(file_stream, media_type="application/pdf", headers=headers)
