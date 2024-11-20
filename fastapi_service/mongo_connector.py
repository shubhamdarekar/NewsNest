import pymongo
import certifi 
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDBManager:
    def __init__(self):
        self.mongo_url = os.getenv('mongo_url')
        self.db_name = os.getenv('db_name')
        self.collection_name = os.getenv('collection_name')
        self.client = None

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.mongo_url, tlsCAFile=certifi.where())
            return self.client
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    def get_database(self):
        if self.client:
            return self.client[self.db_name]
        else:
            raise ValueError("MongoDB client not connected.")

    def get_collection(self):
        if self.client:
            db = self.get_database()
            return db[self.collection_name]
        else:
            raise ValueError("MongoDB client not connected.")
        
    def disconnect(self):
        if self.client:
            self.client.close()