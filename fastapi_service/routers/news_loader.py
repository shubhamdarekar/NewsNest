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


def data_retriever(interested_topics):

    if interested_topics:
        topics_str = ", ".join(["'" + topic.lower() + "'" for topic in interested_topics])
        where_clause = f"WHERE CATEGORY IN ({topics_str})"
    else:
        where_clause = ""

    sql_query = f"""
        SELECT *
        FROM ARTICLES
        {where_clause}
        ORDER BY PUBLISH_DATE DESC
        LIMIT 50;
    """
    result = snowflake_client.execute_query(sql_query)
    return(result)

def news_id(id):

    sql_query = f"""
        SELECT *
        FROM ARTICLES
        WHERE ID={id}
        ORDER BY PUBLISH_DATE DESC;
    """
    try:
        result = snowflake_client.execute_query(sql_query)
    except:
        raise  HTTPException(status_code=401, detail="Invalid NEWS ID")
    return(result)

def top_news():

    sql_query = f"""
        SELECT *
        FROM ARTICLES
        WHERE CATEGORY IN ('top')
        ORDER BY PUBLISH_DATE DESC
        LIMIT 4;
    """
    try:
        result = snowflake_client.execute_query(sql_query)
    except:
        raise  HTTPException(status_code=401, detail="Invalid NEWS ID")
    return(result)

def get_user(email: str):
  
  mongo_manager.connect()
  collection = mongo_manager.get_collection()
  result = collection.find_one({"email": email})
  mongo_manager.disconnect()
  return result

@router.get('/all')
async def news_loader(authorization: str = Header(None)):

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
    interested_topics = [topic for topic, value in user['interests'].items() if value == 1]
    result = data_retriever(interested_topics)

    return {"result": result}

@router.get('/id')
async def news_finder(id:int,authorization: str = Header(None)):

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
    
    result = news_id(id)

    return {"result": result}

@router.get('/top')
async def news_loader(authorization: str = Header(None)):

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
    
    result = top_news()

    return {"result": result}
    

    
