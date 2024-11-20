from fastapi import APIRouter, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
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


def data_retriever():
    sql_query = f"""
        SELECT title, link, description, image_url
        FROM WATCH
        ORDER BY PUBLISH_DATE DESC;
    """
    result = snowflake_client.execute_query(sql_query)
    return(result)

def get_user(email: str):
    mongo_manager.connect()
    collection = mongo_manager.get_collection()
    result = collection.find_one({"email": email})
    mongo_manager.disconnect()
    return result

@router.get('/')
async def news_watch(authorization: str = Header(None)):

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

    result = data_retriever()

    return {"result": result}
