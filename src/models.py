from typing import Optional, Annotated, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Address Model
class Address(BaseModel):
    address_line_1: str = Field(...)
    address_line_2: Optional[str] = None # Optional
    city: str = Field(...)
    country: str = Field(...)
    province_or_state: Optional[str] = None # Optional
    postal_code: str = Field(...)

class Contact(BaseModel):
    phone_number: int = Field(...)
    email: EmailStr = Field(...)

# Payment Model
class Payment(BaseModel):
    currency: str = Field(...)
    discount_percent: Optional[float] = None # Optional
    tax_percent: Optional[float] = None # Optional
    due_amount: float = Field(...)

# Payee Model
class Payee(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    address: Address = Field(...)
    contact: Contact = Field(...)
    status: str = Field(...)
    due_date: str = Field(...)
    payment: Payment = Field(...)
    added_date_utc: datetime = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "address": {
                    "address_line_1": "123 Main St",
                    "address_line_2": "Apt 4B",
                    "city": "New York",
                    "country": "USA",
                    "province_or_state": "NY",
                    "postal_code": "10001"
                },
                "contact": {
                    "phone_number": 1234567890,
                    "email": "john.doe@example.com"
                },
                "status": "overdue",
                "due_date": "2024-12-01",
                "payment": {
                    "currency": "USD",
                    "discount_percent": 10.0,
                    "tax_percent": 8.0,
                    "due_amount": 100.00
                },
                "added_date_utc": 1679356800
            }
        }

# Model for filtering, searching and paging
class Filter(BaseModel):
    first_name: str = None
    last_name: str = None
    city: str = None
    country: str = None
    due_date: str = None

# Update payment model
class PaymentUpdate(BaseModel):
    amount: int = 0
