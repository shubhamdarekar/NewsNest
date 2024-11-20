import streamlit as st

import requests
import configparser
import json

config = configparser.ConfigParser()
config.read('./configuration.properties')
base_url = config['APIs']['base_url']



def signup_and_preferences():
    st.subheader(':red[If you want, you can update your interests...]')

    interests_list = ["Education", "Environment" , "International", "Technology", "Entertainment","United-States",   "Middle-east","Europe",  "India","World",
                      "Football", "Golf", "Job", "Sports",  "Politics",  "Health", "Art","Elections", "Business","Top News","Olympics", "Tennis"] 
   
    st.subheader('Update Interests and Notification Preferences')
    interests = st.multiselect('Interests', options=interests_list, default=[], format_func=lambda x: x)
    notify_about = st.text_input('Notify About', placeholder='Enter what you want to be notified about (e.g., Apple, Elon Musk, Politics)')
    update = st.button('Update Preferences')
    
    interests_dict={}
    
    for interest in interests:
        interests_dict[interest] = 1
    
    
    
    if update:
        url = base_url + '/profile/update' 
        access_token = st.session_state["access_token"]
        token_type = st.session_state["token_type"]
        data = {
            "interests": interests_dict,  # Replace with actual interests data
            "notify_about": notify_about # Replace with actual notify_about data
        }

        headers = {
            'Content-Type': 'application/json',  
            "Authorization": "{} {}".format(token_type, access_token)
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            st.success("Updated preferences")
        else: 
            st.error("Error Try Again")
        


