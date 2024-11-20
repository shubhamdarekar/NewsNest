import functions_framework
from google.cloud import storage
from io import BytesIO
from openai import OpenAI
from pinecone import Pinecone
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import time
import html

@functions_framework.http
def hello_http(request):
    ''' HTTP Cloud Function.
    Extract data from RSS feed
    Embed the news title and check against RSS Feed in PineCone DB
    If new news is present triggre Airflow pipeline to extarct and load data
    
    return -> tuple(status, reason, response)
    '''
    request_json = request.get_json(silent=True)
    request_args = request.args

    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'base_url' in request_json:
        base_url = request_json['base_url']
        category = request_json['category']
        file_name = request_json['file_name']
    elif request_args and 'base_url' in request_args:
        base_url = request_args['base_url']
        category = request_json['category']
        file_name = request_json['file_name']
    else:
        base_url = None

    if base_url is None:
        return "Fail | No url | "

    
    gpt_model = os.environ.get('gpt_model') 
    gpt_key = os.environ.get('gpt_key') 
    pinecone_key = os.environ.get('pinecone_key') 
    index_name = os.environ.get('index_name')
    namespace_today = os.environ.get('namespace_today')
    namespace_yesterday = os.environ.get('namespace_yesterday')
    storage_bucket = os.environ.get('storage_bucket')

    try:
        openai_client = OpenAI(api_key=gpt_key)
        pinecone = Pinecone(api_key=pinecone_key)
        pinecone_index = pinecone.Index(name=index_name)
        storage_client = storage.Client()
        bucket = storage_client.bucket(storage_bucket)

        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"Site NOT Responsing for url: {base_url}")
            return "Fail | Site NOT Responsing | "
        
        content = response.content
        parsed_content = bs(content, 'html.parser')
        if parsed_content == None:
            print(f"No HTML content on url: {base_url}")
            return "Fail | No HTML content | "

        item_content = parsed_content.find_all("item")
        if item_content == []:
            print(f"No HTML <item> component found on url: {base_url}")
            return "Fail | No HTML <item> component | "

        list_news = []
        embedded_data = []
        for item in item_content:
            title = item.find_all("title")[0].get_text()
            link = item.find_all("guid")[0].get_text()
            pubilsh = item.find_all("pubdate")[0].get_text()
            desc_temp = item.find_all("description")[0].get_text().strip()
            desc_temp = html.unescape(desc_temp)
            soup = bs(desc_temp, "html.parser")
            description = soup.find_all("p")[0].get_text()
            img = item.find_all("media:thumbnail")
            if img:
                image = img[0].get("url")
            else:
                image = ""
            temp = {
                "title": title,
                "link": link,
                "pubilsh": pubilsh,
                "description": description,
                "image_url": image,
                "category": category,
                "source": "ABP NEWS"
            }

            embedded_title = openai_client.embeddings.create(
                input=title, 
                model=gpt_model,
            ).data[0].embedding

            res_today = pinecone_index.query(vector=embedded_title, top_k=2, include_metadata=True, namespace=namespace_today)
            res_yesterday = pinecone_index.query(vector=embedded_title, top_k=2, include_metadata=True, namespace=namespace_yesterday)
            res = res_today["matches"] + res_yesterday["matches"]
            
            hasMatch = False
            for i in res:
                if i["score"] >= 0.85:
                    hasMatch = True
                    break

            if hasMatch:
                continue

            timestamp = str(int(time.time()))
            temp_vectors = {
                "id": timestamp,
                "values": embedded_title,
                "metadata":{
                    "title": title
                }
            }
            embedded_data.append(temp_vectors)
            list_news.append(temp)

        if embedded_data == []:
            return "Success | No New Data | "

        pinecone_index.upsert(embedded_data, namespace=namespace_today)
    
        df = pd.DataFrame(list_news)
        in_memory_file = BytesIO()
        in_memory_file.seek(0)
        df.to_csv(in_memory_file, sep="\t", index=False)
        in_memory_file.seek(0)
        blob = bucket.blob(file_name)
        blob.upload_from_file(in_memory_file)

        return f"Success | csv loaded with new news | {file_name}"
    except Exception as e:
        print(e)
        return f"Fail | {e} | "