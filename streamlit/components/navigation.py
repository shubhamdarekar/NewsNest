import streamlit as st
from streamlit_option_menu import option_menu
from components.user_profile import signup_and_preferences
from components.news_dashboard import news_nest_app, news_nest_top, search
from components.watch_news_dashboard import watch_news
from components.google_search import google_search
import configparser
import requests

config = configparser.ConfigParser()
config.read('./configuration.properties')
base_url = config['APIs']['base_url']

def tabs():
  options = ["News Dashboard", "Watch News","Google Search","User Profile"]
  icons = ['','', '',''] 

  with st.expander("See Notifications"):
    url = base_url + '/notify'
    access_token = st.session_state["access_token"]
    token_type = st.session_state["token_type"]
    # Making the POST request
    headers = {
        "Authorization": "{} {}".format(token_type, access_token),
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
      if response.json()["notifications"] != []:
        for result in response.json()["notifications"]:
          st.markdown(result["TITLE"] + ' ' + f"[View Full News]({result['LINK']})")
      else:
        st.write("No Notification")
    else:
      st.write("Request Not Processed")
  nav_menu = option_menu(None, options, 
    icons=icons, 
    menu_icon="cast", 
    key='nav_menu',
    default_index=0, 
    orientation="horizontal"
  )

  nav_menu

  if st.session_state["nav_menu"] == "News Dashboard" or st.session_state["nav_menu"]==None:
    search()
    news_nest_top()
    news_nest_app()
  elif st.session_state["nav_menu"] == "Watch News":
    watch_news()
  elif st.session_state["nav_menu"] == "Google Search":
    google_search()
  elif st.session_state["nav_menu"] == "User Profile":
    signup_and_preferences()
