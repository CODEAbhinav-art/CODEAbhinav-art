import streamlit as st
import random
import time
# import requests
from google import genai

base_prompt="""hello i am designing a chatbot for student accomodation so only give short and to the point responses accordingly,
               based on these data:Property Name: [Student PG in Vadodara, 1BHK near MSU, Shared Hostel Room, 2BHK Apartment, Studio Apartment],Location: [Vadodara, Vadodara, Mumbai,Ahmedabad,Vadodara],Rent (INR): [6000, 12000, 5000, 18000, 8000],Duration: [1 Month, 3 Months, 6 Months, 12 Months, 3 Months],"Owner Contact": ["ramesh_rentals@gmail.com", "Kishan_houses@gmail.com", "satyam_pgs@gmail.com", "vijay.rentals@example.com", "info@modernliving.in"],
               meals and other bills not include in the rent,to book an accomodations fill the form present on the main website: http://10.201.113.127:8502
               ,if you dont have answer say:sorry,I didn't understood the query please contact: renters@gmail.com for further information,also i am adding previous prompts if any (here):"""

saved_base_prompt = []

def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def bot_response(content):
    client = genai.Client(api_key="AIzaSyBT4spBTSfjH3kwP3D4VdZqKdU2AtJ5ux0")
    response_text = client.models.generate_content(
        model="gemini-2.0-flash", contents=content
    )
    for word in response_text.text.split():
        yield word + " "
        time.sleep(0.05)


st.title("Simple chat")

with st.chat_message("AI"):
    st.write("Hello 👋")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

if prompt != None:
    prompt1= base_prompt +"("+ prompt + ")" + "respond to this question based on previous lines-> QUESTION:"
    saved_base_prompt.append(prompt1)
    final_prompt= saved_base_prompt[-1] + prompt


with st.chat_message("assistant"):
    if prompt:
        response=st.write_stream(bot_response(final_prompt))
    else:
        response = st.write_stream(response_generator())


st.session_state.messages.append({"role": "assistant", "content":response})






























