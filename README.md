# Final Project - NewsNest

## Live application Links


- Airflow: TBD
- Fast API Auth: TBD
- Fast API Services: TBD
- Streamlit Application: TBD

## Problem Statement 
Accessing and analysing diverse news sources is cumbersome, leading to information overload and a lack of personalised experiences. Manual scanning and filtering news based on interests is time-consuming, and a real-time notifier on latest news tailored to individual interests is required. A scalable data engineering solution is needed to automate news scraping from reliable sources, processing, and delivery, ensuring personalised, real-time updates while prioritising data integrity and user engagement.

## Project Goals
1. Provide Comprehensive and Trustworthy News: The primary goal of the project is to offer users a comprehensive and trustworthy news aggregation platform. This involves sourcing news articles from reputable outlets like The New York Times, CBC News, ABP News, and ABC News to ensure accuracy and reliability in the information provided.
2. Real-Time Updates: The project aims to deliver real-time summaries of current events across various topics, including politics, business, technology, and entertainment. The goal is to keep users informed about the latest developments as they occur.
3. Personalization: Another goal is to provide personalized news experiences for users. This includes allowing individuals to customize their news feed based on their interests, ensuring that they receive content relevant to their preferences.
4. Automation and Scalability: The project aims to develop a scalable data engineering solution for automating news scraping from reliable sources. This involves periodic scraping of news, parallel scraping to improve efficiency, and ensuring scalability to handle increasing volumes of data.
5. Alert System: Implementing an alert system for notifying users about real-time updates is also a goal of the project. This ensures that users are promptly informed about important news developments.
6. Avoiding Repetitive News: To enhance user experience, the project aims to avoid repetitive news by implementing mechanisms to filter out duplicate or redundant content from multiple sources.

## Technologies Used
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Apache Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-%232496ED?style=for-the-badge&logo=Docker&color=blue&logoColor=white)](https://www.docker.com)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-%234169E1?style=for-the-badge&logo=MongoDB&logoColor=%234169E1&color=black)](https://www.postgresql.org)
[![Snowflake](https://img.shields.io/badge/snowflake-%234285F4?style=for-the-badge&logo=snowflake&link=https%3A%2F%2Fwww.snowflake.com%2Fen%2F%3F_ga%3D2.41504805.669293969.1706151075-1146686108.1701841103%26_gac%3D1.160808527.1706151104.Cj0KCQiAh8OtBhCQARIsAIkWb68j5NxT6lqmHVbaGdzQYNSz7U0cfRCs-STjxZtgPcZEV-2Vs2-j8HMaAqPsEALw_wcB&logoColor=white)
](https://www.snowflake.com/en/?_ga=2.41504805.669293969.1706151075-1146686108.1701841103&_gac=1.160808527.1706151104.Cj0KCQiAh8OtBhCQARIsAIkWb68j5NxT6lqmHVbaGdzQYNSz7U0cfRCs-STjxZtgPcZEV-2Vs2-j8HMaAqPsEALw_wcB)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Pinecone](https://img.shields.io/badge/Pinecone-8C54FF?style=for-the-badge&logo=pinecone&logoColor=white)](https://www.pinecone.io/)
[![SERP API](https://img.shields.io/badge/SERP_API-009688?style=for-the-badge&logo=google&logoColor=white)](https://serpapi.com/)
[![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apache%20kafka&logoColor=white)](https://kafka.apache.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-00BFFF?style=for-the-badge&logo=python&logoColor=white)](https://pydantic-docs.helpmanual.io/)
[![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=python&logoColor=white)](https://pytest.org/)


## Architecture Diagram
Data FLow:

![alt text](TBD)

Kafka Stream:

![alt text](TBD)

API:

![alt text](TBD)

```
📦 NewsNest
├─ Architecture Diagram
│  ├─ Kafka.png
│  ├─ Scrapping - load.png
│  ├─ architecture_diagram (1).ipynb
│  └─ user diagram
├─ airflow
│  ├─ dags
│  │  ├─ configuration.properties.example
│  │  ├─ dag_abcnews.py
│  │  ├─ dag_abpnews.py
│  │  ├─ dag_cbcnews.py
│  │  ├─ dag_notification.py
│  │  └─ dag_nytimes.py
│  ├─ Dockerfile
│  ├─ docker-compose.yml
│  └─ requirements.txt
├─ cloud_function
│  ├─ data_cleaning
│  │  ├─ main.py
│  │  └─ requirements.txt
│  ├─ data_load
│  │  ├─ main.py
│  │  └─ requirements.txt
│  ├─ kafka_notification
│  │  ├─ main.py
│  │  └─ requirements.txt
│  ├─ keyword_extraction
│  │  ├─ main.py
│  │  └─ requirements.txt
│  └─ webscrapping
│     ├─ main.py
│     └─ requirements.txt
├─ fastapi_auth
│  ├─ Dockerfile
│  ├─ docker-compose.yml
│  ├─ main.py
│  └─ requirements.txt
├─ fastapi_service
│  ├─ routers
│  │  ├─ __init__.py
│  │  ├─ news_loader.py
│  │  ├─ news_watch.py
│  │  ├─ notifications.py
│  │  ├─ profile.py
│  │  └─ search.py
│  ├─ Dockerfile
│  ├─ docker-compose.yml
│  ├─ main.py
│  ├─ mongo_connector.py
│  ├─ requirements.txt
│  ├─ serp.py
│  ├─ snowflake_connector.py
│  ├─ test_fastapi.py
│  └─ util.py
├─ kafka
│  └─ docker-compose.yml
├─ scripts
│  └─ kafka_consumer.py
├─ streamlit
│  ├─ components
│  │  ├─ google_search.py
│  │  ├─ login_signup.py
│  │  ├─ navigation.py
│  │  ├─ news_dashboard.py
│  │  ├─ user_profile.py
│  │  └─ watch_news_dashboard.py
│  ├─ Dockerfile
│  ├─ config.py
│  ├─ configuration.properties.example
│  ├─ docker-compose.yml
│  ├─ main.py
│  └─ requirements.txt
└─ README.md
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)

## Pre requisites
1. Python Knowledge
2. Pinecone API Key
3. Openai API Key
4. Docker Desktop
5. MongoDB database knowledge
6. Vector database knowledge
8. Streamlit knowledge
9. Airflow pipeline knowledge
10. Google Cloud Platform account and hosting knowledge


## How to run Application Locally
1. Clone the GitHub Project
2. Add configuration.properties
3. Load Cloud Functions with main.py
4. Link the cloud functions with airflow conifguration.properties
5. Run Airflow locally using the docker image
6. run the docker image for fasapi-auth
7. run the docker image for fastapi-service
8. run the docker image for setreamlit


## References

- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- https://diagrams.mingrammer.com/
- https://cloud.google.com
- https://app.snowflake.com/
