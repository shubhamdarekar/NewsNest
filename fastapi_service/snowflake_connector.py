from snowflake.connector import connect, DictCursor
from dotenv import load_dotenv
import os   

class SnowflakeConnector:
    def __init__(self):
        load_dotenv()
        self.snowflake_config = {
            "user": os.getenv('sf_user'),
            "password": os.getenv('sf_password'),
            "account": os.getenv('sf_account'),
            "database": os.getenv('sf_database'),
            "schema": os.getenv('sf_schema')
        }
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = connect(**self.snowflake_config)

    def execute_query(self, query):
        if not self.connection:
            self.connect()
        with self.connection.cursor(DictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
