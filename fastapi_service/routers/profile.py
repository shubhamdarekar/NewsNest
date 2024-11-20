from fastapi import FastAPI, APIRouter, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import pandas as pd
import jwt
import os
from snowflake_connector import SnowflakeConnector
from mongo_connector import MongoDBManager


load_dotenv()

router = APIRouter()
snowflake_client = SnowflakeConnector()
mongo_manager = MongoDBManager()

# JWT config
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

# oauth2 scheme
tokenUrl = os.getenv('tokenUrl')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=tokenUrl)

# password encryption
schemes = os.getenv('schemes')
deprecated = os.getenv('deprecated')
pwd_context = CryptContext(schemes=schemes, deprecated=deprecated)

def get_user(email: str):
  
  mongo_manager.connect()
  collection = mongo_manager.get_collection()
  result = collection.find_one({"email": email})
  mongo_manager.disconnect()
  return result

def update_user(email: str, new_details: dict):
    mongo_manager.connect()
    collection = mongo_manager.get_collection()
    try:
        collection.update_one({"email": email}, {"$set": new_details})
        status = 1
    except:
        status = 0 
    mongo_manager.disconnect()
    return status


@router.get('/view')
async def profile_view(authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM, ])
        email: str = token_decode.get("sub")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token has expired")
    
    user = get_user(email)
    return {"interest": user['interests'], "notification": user["notifications"]}

@router.post('/update')
async def profile_update(payload:dict, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM, ])
        email: str = token_decode.get("sub")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token has expired")
    notify_about = list(payload["notify_about"].split(", "))
    to_update = {"interests": payload["interests"], "notify_about": notify_about}
    status = update_user(email, to_update)

    return {"message": status}

    

    
