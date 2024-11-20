import functions_framework
from google.cloud import storage
from io import BytesIO
import pandas as pd
import os
import spacy

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

    clean_bucket = os.environ.get('clean_bucket')
    keyword_bucket = os.environ.get('keyword_bucket')

    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    
    def extract_keywords(text):
        doc = nlp(text)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
        str_keywords = ",".join(keywords)
        return str_keywords
    
    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(clean_bucket)
        blob = bucket.blob(file_name)

        bucket_keyword= storage_client.bucket(keyword_bucket)
        blob_keyword = bucket_keyword.blob(file_name)

        byte_stream = BytesIO()
        blob.download_to_file(byte_stream)
        byte_stream.seek(0)
        
        df = pd.read_csv(byte_stream, sep="\t")
        byte_stream.close()
        list_dict = df.to_dict(orient='records')

        keyword_list = []
        for row in list_dict:
            str_keywords = extract_keywords(row["title"])
            row["keywords"] = str_keywords
            keyword_list.append(row)
            
        print(keyword_list)

        if keyword_list != []:
            df_clean = pd.DataFrame(keyword_list)
            in_memory_file = BytesIO()
            in_memory_file.seek(0)
            df_clean.to_csv(in_memory_file, sep="\t", index=False)
            in_memory_file.seek(0)
            blob_keyword.upload_from_file(in_memory_file)
            in_memory_file.close()

        return "Success"
        
    except Exception as e:
        print(e)
        return "Fail"


