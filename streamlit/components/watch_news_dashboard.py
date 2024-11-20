import streamlit as st
from streamlit.components.v1 import iframe
import configparser
import requests


config = configparser.ConfigParser()
config.read('./configuration.properties')
base_url = config['APIs']['base_url']


def watch_news():
    st.subheader(":red[Watch Latest News Shorts]")
    
    url = base_url + '/watch'
    access_token = st.session_state["access_token"]
    token_type = st.session_state["token_type"]
    # Making the POST request
    headers = {
        "Authorization": "{} {}".format(token_type, access_token),
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    
    set_of_frozensets = {frozenset(d.items()) for d in response.json()['result']}
    unique_list_of_dicts = [dict(fs) for fs in set_of_frozensets]
    col_count = 4
    for i in range(0, len(unique_list_of_dicts), col_count):
        cols = st.columns(col_count)
        for j in range(col_count):
            if i + j < len(unique_list_of_dicts):
                with cols[j]:
                    iframe(unique_list_of_dicts[i + j]["LINK"], width=425, height=600, scrolling=True)


