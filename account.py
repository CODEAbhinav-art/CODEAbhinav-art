import streamlit as st
import firebase_admin
import os
from firebase_admin import credentials,auth

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the credentials file
cred_path = os.path.join(script_dir, 'renters-7257e-daa76c69c975.json')

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)



# cred=credentials.Certificate('pythoproject\renters-7257e-daa76c69c975.json')
# # firebase_admin.initialize_app(cred)

def app():
   st.title('welcome to :red[Renters account]')
   
   choice=st.selectbox('login/signup',['login','signup'])
   if choice=='login':
     email=st.text_input('Email Address')
     password=st.text_input('password',type='password')
     
     st.button('login')
   else:
     email=st.text_input('Email Address')
     password=st.text_input('password',type='password')
     username=st.text_input('enter your unique username')
     if st.button('create my account'):
        user=auth.create_user(email=email,password=password,uid=username)
        st.success('user created successfully')
        st.markdown('please login to continue')
        st.balloons()








