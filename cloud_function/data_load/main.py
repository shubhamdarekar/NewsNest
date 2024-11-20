import functions_framework
import os
import snowflake.connector


@functions_framework.http
def load_data(request):
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

    merge_query = f'''MERGE INTO articles a
        USING (SELECT $1 title,
                        $2 link,
                        $3 description,
                        $4 image_url,
                        $5 category,
                        $6 source,
                        $7 publish_date,
                        $8 id, 
                        $9 keywords from @stage_gcs_bucket_keyword/{file_name} (FILE_FORMAT => news_ff)) s
        ON a.link = s.link
        WHEN NOT MATCHED THEN
        INSERT (title, link, description, image_url, category, source, publish_date, id, keywords)
        VALUES (s.title, s.link, s.description, s.image_url, s.category, s.source, s.publish_date, s.id, s.keywords);
    '''
    
    try:
        cursor = conn.cursor()
        cursor.execute(merge_query)
        cursor.close()

        return "Success"
        
    except Exception as e:
        print(e)
        return "Fail"


