import functions_framework
from google.cloud import storage
from io import BytesIO
import pandas as pd
import os
import time
from pydantic import BaseModel, Field
from typing import Optional
from dateutil import parser
import snowflake.connector
import random

class Article(BaseModel):
    title: str
    link: str
    pubilsh: str
    description: str
    category: str
    source: str
    image_url: Optional[str] = Field(default = None)

@functions_framework.http
def clean_data(request):
    ''' HTTP Cloud Function.
    read file from sourde bucket clean the data and load the clean data into destination bucket
    '''
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'file_name' in request_json:
        file_name = request_json['file_name']
    elif request_args and 'file_name' in request_args:
        file_name = request_json['file_name']
    else:
        file_name = None

    if file_name is None:
        return "Fail"
    
    watch_file = "watch/" + file_name
    storage_bucket = os.environ.get('storage_bucket')
    clean_bucket = os.environ.get('clean_bucket')
    SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_USER = os.environ.get('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.environ.get('SNOWFLAKE_PASSWORD')
    SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE')
    SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_SCHEMA')

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(storage_bucket)
        blob = bucket.blob(file_name)

        bucket_clean = storage_client.bucket(clean_bucket)
        blob_clean = bucket_clean.blob(file_name)

        byte_stream = BytesIO()
        blob.download_to_file(byte_stream)
        byte_stream.seek(0)
        
        df = pd.read_csv(byte_stream, sep="\t")
        byte_stream.close()
        list_dict = df.to_dict(orient='records')

        clean_list = []
        watch_list = []
        for row in list_dict:
            timestamp = str(int(time.time())) + str(random.randint(1,100))
            if "LIVE:" in row["title"]:
                continue
            for i in row:
                row[i] = row[i].strip()
            try:
                date_str = row["pubilsh"]
                if "EDT" in date_str:
                    date_str.replace("EDT", "-0400")
                row["publish"] = parser.parse(date_str)
                del row["pubilsh"]
                row["id"] = timestamp
                if "WATCH:" in row["title"]:
                    watch_list.append(row)
                else:
                    clean_list.append(row)    
            except Exception as e:
                print(e) 
                print(f"removing row {row}")
        
        print(clean_list)
        print(watch_list)

        if clean_list != []:
            df_clean = pd.DataFrame(clean_list)
            in_memory_file = BytesIO()
            in_memory_file.seek(0)
            df_clean.to_csv(in_memory_file, sep="\t", index=False)
            in_memory_file.seek(0)
            blob_clean.upload_from_file(in_memory_file)
            in_memory_file.close()

        if watch_list != []:
            df_watch = pd.DataFrame(watch_list)
            in_memory_file_watch = BytesIO()
            in_memory_file_watch.seek(0)
            df_watch.to_csv(in_memory_file_watch, sep="\t", index=False)
            in_memory_file_watch.seek(0)
            blob_watch = bucket_clean.blob(watch_file)
            blob_watch.upload_from_file(in_memory_file_watch)
            in_memory_file_watch.close()

            cursor = conn.cursor()
            cursor.execute(f"COPY INTO watch FROM '@stage_gcs_bucket_news/{watch_file}' FILE_FORMAT = (FORMAT_NAME = 'news_ff') ON_ERROR = 'CONTINUE'")
            cursor.close()

        return "Success"
        
    except Exception as e:
        print(e)
        return "Fail"


