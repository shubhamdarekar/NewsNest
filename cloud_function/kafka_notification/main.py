import functions_framework
import os
import snowflake.connector
from kafka import KafkaProducer
import json

@functions_framework.http
def kafka_notification(request):
    ''' HTTP Cloud Function.
    read file from sourde bucket clean the data and load the clean data into destination bucket
    '''

    SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_USER = os.environ.get('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.environ.get('SNOWFLAKE_PASSWORD')
    SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE')
    SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_SCHEMA')
    kafka_service = os.environ.get("kafka_service")
    kafka_topic = os.environ.get("kafka_topic")

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    
    producer = KafkaProducer(
        bootstrap_servers=kafka_service,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    merge_query = f'''select keywords, id, title from articles where insert_time >= DATEADD(minute, -15, CURRENT_TIMESTAMP());'''
    
    try:
        cursor = conn.cursor()
        cursor.execute(merge_query)
        result = cursor.fetchall()
        for keywords, id, title in result:
            if kafka_topic:
                data = {
                    "id": id,
                    "keywords": keywords.split(","),
                    'title': title
                }
                producer.send(kafka_topic, data)
                producer.flush()
        cursor.close()
        return "Success"
    except Exception as e:
        print(e)
        return "Fail"


