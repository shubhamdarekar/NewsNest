import streamlit as st
import configparser
import requests
from PIL import Image
from io import BytesIO
from streamlit_modal import Modal

config = configparser.ConfigParser()
config.read('./configuration.properties')
base_url = config['APIs']['base_url']

modal_top = Modal("Description Summary", key="modal")


def show_modal(modal_top, news_data):
    open_modal = st.button(news_data["Title"])

    if open_modal:
        st.session_state["modal_desc"] = news_data["Description"]
        st.session_state["modal_link"] = news_data["Link"]
        modal_top.open()

def news_nest_top():
    try:
        st.subheader(":red[NewsNest: Top News]")
        
        if modal_top.is_open():
            with modal_top.container():
                st.write(st.session_state["modal_desc"])
                st.markdown(f'[View Full News]({st.session_state["modal_link"]})')
                
        url = base_url + '/news/top'
        access_token = st.session_state["access_token"]
        token_type = st.session_state["token_type"]
        # Making the POST request
        headers = {
            "Authorization": "{} {}".format(token_type, access_token),
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        
        news_data = []
        for result in response.json()['result']:
            formatted_result = {}
            formatted_result['Title'] = result.get('TITLE',"")
            formatted_result['Link'] = result.get('LINK',"")
            formatted_result['Description'] = result.get('DESCRIPTION',"")
            formatted_result['Image_url'] = result.get('IMAGE_URL',"")
            formatted_result['Source'] = result.get('SOURCE',"")
            formatted_result['Publish_Date'] = result.get('PUBLISH_DATE',"")
            news_data.append(formatted_result)
        
        col_count = 4
        for i in range(0, len(news_data), col_count):
            cols = st.columns(col_count)
            for j in range(col_count):
                if i + j < len(news_data):
                    with cols[j]:
                        markdown_str = f'<img src="{news_data[i + j]["Image_url"]}" width="425" height="200">'
                        st.markdown(markdown_str, unsafe_allow_html=True)
                        show_modal(modal_top, news_data[i + j])
    except Exception as e:
        pass

def news_nest_app():
    try:
        st.subheader(":red[NewsNest: Interests]")
        
        if modal_top.is_open():
            with modal_top.container():
                st.write(st.session_state["modal_desc"])
                st.markdown(f'[View Full News]({st.session_state["modal_link"]})')
                
        url = base_url + '/news/all'
        access_token = st.session_state["access_token"]
        token_type = st.session_state["token_type"]
        # Making the POST request
        headers = {
            "Authorization": "{} {}".format(token_type, access_token),
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        news_data = []
        for result in response.json()['result']:
            formatted_result = {}
            formatted_result['Title'] = result.get('TITLE',"")
            formatted_result['Link'] = result.get('LINK',"")
            formatted_result['Description'] = result.get('DESCRIPTION',"")
            formatted_result['Image_url'] = result.get('IMAGE_URL',"")
            formatted_result['Source'] = result.get('SOURCE',"")
            formatted_result['Publish_Date'] = result.get('PUBLISH_DATE',"")
            news_data.append(formatted_result)
        
        col_count = 4
        for i in range(0, len(news_data), col_count):
            cols = st.columns(col_count)
            for j in range(col_count):
                if i + j < len(news_data):
                    with cols[j]:
                        markdown_str = f'<img src="{news_data[i + j]["Image_url"]}" width="425" height="200">'
                        st.markdown(markdown_str, unsafe_allow_html=True)
                        show_modal(modal_top, news_data[i + j])
    except Exception as e:
        pass
    
def fetch_data(search_term):
    try:
        # Example API endpoint for fetching data based on search term
        url = base_url + '/search/db?to_search=' + search_term.replace(" ", "%20")
        access_token = st.session_state["access_token"]
        token_type = st.session_state["token_type"]
        # Making the POST request
        headers = {
            "Authorization": "{} {}".format(token_type, access_token),
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        pass

def search():
    try:
        search_term = st.text_input(':blue[Search News:]', placeholder='Search News:')
        if search_term and len(search_term) > 2:
            data = fetch_data(search_term)["result"]
            if data:
                # st.write(data)
                st.subheader(":red[NewsNest: Search Result]")
                news_data = []
                for result in data:
                    formatted_result = {}
                    formatted_result['Title'] = result.get('TITLE',"")
                    formatted_result['Link'] = result.get('LINK',"")
                    formatted_result['Description'] = result.get('DESCRIPTION',"")
                    formatted_result['Image_url'] = result.get('IMAGE_URL',"")
                    formatted_result['Source'] = result.get('SOURCE',"")
                    formatted_result['Publish_Date'] = result.get('PUBLISH_DATE',"")
                    news_data.append(formatted_result)
                
                col_count = 4
                for i in range(0, len(news_data), col_count):
                    cols = st.columns(col_count)
                    for j in range(col_count):
                        if i + j < len(news_data):
                            with cols[j]:
                                markdown_str = f'<img src="{news_data[i + j]["Image_url"]}" width="425" height="200">'
                                st.markdown(markdown_str, unsafe_allow_html=True)
                                show_modal(modal_top, news_data[i + j])
            else:
                st.write("No Data for search")
    except Exception as e:
        pass