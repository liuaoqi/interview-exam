import logging

import uvicorn
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from dotenv import dotenv_values
from pymongo import MongoClient

from app_config import BASE_APP, HOST, PORT, RELOAD, LOG_LEVEL

from routing import router as payment_router
# # Authentication
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel

config = dotenv_values(".env")
logging.basicConfig(level=logging.INFO)

# # Authentication
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    yield
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(payment_router, tags=["payments"], prefix="/payment")

if __name__ == "__main__":
    uvicorn.run(BASE_APP, host=HOST, port=PORT, reload=RELOAD, log_level=LOG_LEVEL)