import streamlit as st
import requests
import configparser
from streamlit_modal import Modal
import requests
from PIL import Image
from io import BytesIO

config = configparser.ConfigParser()
config.read('./configuration.properties')
base_url = config['APIs']['base_url']


def show_modal(news_data):
    st.write(news_data["TITLE"])
    st.markdown(f'[View Full News]({news_data["LINK"]})')


def google_search():
    
    
    st.subheader(":red[Read latest news on google...]")
    
    with st.form(key='search', clear_on_submit=True):
        google_search = st.text_input(':blue[Search on google news:]', placeholder='Search on google news:')
        sub = st.form_submit_button('Search')
        
        if sub:
            url = base_url + "/search/serp?to_search=" + google_search.replace(" ", "%20")
            print(url)
            access_token = st.session_state["access_token"]
            token_type = st.session_state["token_type"]
            # Making the POST request
            headers = {
                "Authorization": "{} {}".format(token_type, access_token),
                'Content-Type': 'application/json',
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                search_news = response.json()["result"]
                col_count = 4
                for i in range(0, len(search_news), col_count):
                    cols = st.columns(col_count)
                    for j in range(col_count):
                        if i + j < len(search_news):
                            with cols[j]:
                                response_img = requests.get(search_news[i + j]["IMAGE_URL"])
                                if response_img.status_code == 200:
                                    # Open the image using PIL
                                    image = Image.open(BytesIO(response_img.content))
                                    # Display the image in Streamlit
                                    st.image(image, use_column_width=True)
                                show_modal(search_news[i + j])
            else:
                st.write("No News returned for this Search")