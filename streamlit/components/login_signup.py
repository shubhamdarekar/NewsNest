import streamlit as st
import requests
import json
import re
from streamlit_option_menu import option_menu
# from news_dashboard import news_nest_app'
import configparser

config = configparser.ConfigParser()
config.read('./configuration.properties')
base_url = config['APIs']['base_url_auth']


def menu_login():
    ''' navigation menu for login/signup '''
    st.title("NewsNest: Curated Summaries Hub")
    login_menu = option_menu(None, ["Login", "Sign Up"], 
        icons=['person-fill', "person-plus-fill"], 
        menu_icon="cast", 
        key='login_menu',
        default_index=0, 
        orientation="horizontal"
    )
    login_menu
    if st.session_state["login_menu"] == "Login" or st.session_state["login_menu"] == None:
        login()
    elif st.session_state["login_menu"] == "Sign Up":
        sign_up()


def sign_up():
    ''' Sign up form '''
    interests_list = ["Education", "Environment" , "International", "Technology", "Entertainment","United-States",   "Middle-east","Europe",  "India","World",
                      "Football", "Golf", "Job", "Sports",  "Politics",  "Health", "Art","Elections", "Business","Top News","Olympics", "Tennis"] 
    # notify_about_list = st.text_input(':blue[Notify About]', placeholder='Enter what you want to be notified about (e.g., Science, Technology, Politics)')
        
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':red[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')
        
        
        interests = st.multiselect(':blue[Interests]', options=interests_list, default=[], format_func=lambda x: x)
        
        notify_about = st.text_input(':blue[Notify About]', placeholder='Enter what you want to be notified about (e.g., Apple, Elon Musk, Politics)')
        
        btn1, btn2, btn3 = st.columns([3, 1, 3])

        with btn2:
            sub = st.form_submit_button('Sign Up')

        if sub:
            # Validate all fields including the new ones
            if validate_email_signup(email) and validate_username_signup(username) and validate_password_signup(password1, password2) and validate_interests(interests) and validate_notify_about(notify_about):
                url = base_url + '/signup' 

                interests_dict = {}
                for inter in interests:
                    interests_dict[inter] = 1

                # Create payload including new fields
                payload = {
                    "email": email,
                    "username": username,
                    "password": password1,
                    "interests": interests_dict,
                    "notify_about": notify_about
                }

                json_data = json.dumps(payload)

                headers = {
                    'Content-Type': 'application/json',  
                }
                response = requests.post(url, headers=headers, data=json_data)

                if response.status_code == 200:
                    st.success("User Registered!")
                else: 
                    st.error("Error Try Again")


def login():
    ''' Login form '''
    
    with st.form(key='login', clear_on_submit=True):
        st.subheader(':red[Login]')
        username = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        password = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        btn1, btn2, btn3 = st.columns([3, 1, 3])
        with btn2:
            sub = st.form_submit_button('Login')

        if sub:
            if validate_username(username) and validate_password(password):
                url = base_url + '/login'
                payload = {
                    'email': username, 
                    'password': password
                }
                json_data = json.dumps(payload)
                headers = {
                    'Content-Type': 'application/json',
                }
                response = requests.post(url, headers=headers, data=json_data)
                if response.status_code == 200:
                    st.session_state["auth_status"] = True
                    st.session_state["username"] = username
                    st.session_state["access_token"] = response.json()["access_token"]
                    st.session_state["token_type"] = response.json()["token_type"]
                    st.rerun()


def validate_email_signup(email):
    ''' Validate email for signup '''
    # Regular expression for email validation
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if email:
        if re.match(regex, email):
            return True
        else:
            st.warning('Invalid Email')
            return False
    else:
        st.warning('Enter an Email')
        return False


def validate_username_signup(username):
    ''' Validate username for signup '''
    if username:
        if len(username) > 3:
            return True
        else:
            st.warning('Invalid Username')
            return False
    else:
        st.warning('Enter an Username')
        return False


def validate_password_signup(password1, password2):
    ''' Validate password for signup '''
    if password1:
        if password2:
            if password1 == password2:
                return True
            else:
                st.warning("Password Don't Match")
                return False
        else:
            st.warning('Enter Confirm Password')
            return False
    else:
        st.warning('Enter Password')
        return False


def validate_username(username):
    ''' Validate username '''
    if username:
        return True
    else:
        st.warning('Enter an Username')
        return False


def validate_password(password):
    ''' Validate password '''
    if password:
        return True
    else:
        st.warning('Enter Password')
        return False


def validate_interests(interests):
    ''' Validate interests '''
    if interests:
        return True
    else:
        st.warning('Enter Your Interests')
        return False

def validate_notify_about(notify_about):
    ''' Validate notify_about '''
    if notify_about:
        return True
    else:
        st.warning('Enter Your Preferences')
        return False