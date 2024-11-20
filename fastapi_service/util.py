from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import pymongo
import certifi 
import jwt
import os

load_dotenv()

# JWT config
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Mongo config
mongo_url = os.getenv('mongo_url')
db_name = os.getenv('db_name')
collection_name = os.getenv('collection_name')

# oauth2 scheme
tokenUrl = os.getenv('tokenUrl')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=tokenUrl)

# password encryption
schemes = os.getenv('schemes')
deprecated = os.getenv('deprecated')
pwd_context = CryptContext(schemes=schemes, deprecated=deprecated)

def get_mongo_clien():
    try:
        connection = pymongo.MongoClient(mongo_url,tlsCAFile=certifi.where())
        return connection
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    
def verify_password(plain_password, hashed_password):
  ''' verify the passowrd for login '''
  return pwd_context.verify(plain_password, hashed_password)

def get_user(email: str):
  ''' get user data from db with email '''
  client = get_mongo_clien()
  db = client[db_name]
  collection = db[collection_name]
  result = collection.find_one({"email": email})
  client.close()
  return result

def create_user(email: str, password: str, username: str, interests:dict, notify_about: str, notifications: list):
  ''' add new user in db '''
  client = get_mongo_clien()
  db = client[db_name]
  collection = db[collection_name]
  
  hashed_password = pwd_context.hash(password)

  news_categories = {
      'travel': 0,
      'sports': 0,
      'international': 0,
      'technology': 0,
      'health': 0,
      'us': 0,
      'top': 0,
      'politics': 0,
      'entertainment': 0,
      'europe': 0,
      'football': 0,
      'golf': 0,
      'middleeast': 0,
      'job': 0,
      'environment': 0,
      'world': 0,
      'education': 0,
      'elections': 0,
      'india': 0,
      'business': 0,
      'olympics': 0,
      'art': 0,
      'tennis': 0
  }
  
  notify_about = notify_about.split(", ")

  document = {
    "email": email,
    "username": username,
    "password": hashed_password,
    "interests": interests,
    "notify_about": notify_about,
    "views": news_categories,
    "notifications": notifications

  }
  try:
    collection.insert_one(document)
    status =1
    client.close()
  except:
    status = 0

  return status


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  ''' Create access token '''
  to_encode = data.copy()
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt