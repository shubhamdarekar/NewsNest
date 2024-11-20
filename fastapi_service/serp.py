from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import datetime


class NewsSearch:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('serp_api_key')
        self.search_engine = os.getenv('serp_search_engine')

    def search_news(self, query):
        self.query = query
        params = {
            "engine": self.search_engine,
            "q": self.query,
            "api_key": self.api_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results["news_results"]

        news = []

        for item in news_results[:5]:
            new_item = {
                "TITLE": item['title'],
                "LINK": item['link'],
                "IMAGE_URL": item['thumbnail'],
                "SOURCE": item['source']['name'].upper(),
                "PUBLISH_DATE": datetime.datetime.strptime(item['date'], "%m/%d/%Y, %I:%M %p, +0000 UTC").isoformat()
            }
            news.append(new_item)

        return news
