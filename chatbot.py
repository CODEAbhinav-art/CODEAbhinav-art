import streamlit as st
import time
from google import genai
import database

base_faq_responses = {
    "hello": "Hello there! Welcome to Renters. How can I help you find the perfect place today?",
    "hi": "Greetings! What rental questions do you have for me?",
    "hey": "Hey! Looking for rentals? I'm here to assist.",
    "rentals": "You can browse all our available rental listings on the 'Property Listings' page. Filter by location and rent to find your ideal property.",
    "properties": "Looking for properties? Visit 'Property Listings' to see what's available.",
    "book a property": "To book a property, go to the 'Property Listings' page, filter the listings, and you'll find a booking form below the property details.",
    "booking": "Property bookings can be made on the 'Property Listings' page. See a listing you like? Book it there!",
    "leave a review": "We value your feedback! You can leave a review on the 'Leave a Review' page.",
    "reviews": "Want to leave feedback? Use the 'Leave a Review' page.",
    "contact": "For property-specific inquiries, you'll find the owner's contact information in each listing. For general questions, feel free to ask me!",
    "help": "I can help you with finding rental listings, booking properties, and leaving reviews. What do you need help with today?",
}

def get_property_data_text():
    properties = database.get_properties()
    prop_names = [p[1] for p in properties]
    locations = [p[2] for p in properties]
    rents = [p[3] for p in properties]
    durations = [p[4] for p in properties]
    contacts = [p[5] for p in properties]

    text = "Property Name: " + str(prop_names) + ", "
    text += "Location: " + str(locations) + ", "
    text += "Rent (INR): " + str(rents) + ", "
    text += "Duration: " + str(durations) + ", "
    text += '"Owner Contact": ' + str(contacts)
    return text

def bot_response(content):
    client = genai.Client(Api key vs code me hai)
    response_text = client.models.generate_content(
        model="gemini-2.0-flash", contents=content
    )
    for word in response_text.text.split():
        yield word + " "
        time.sleep(0.05)

def clear_input():
    st.session_state.user_input = ""

def app():
    st.title("Rental Assistant Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display common FAQs as buttons
    st.markdown("### Common FAQs")
    cols = st.columns(3)
    faq_keys = list(base_faq_responses.keys())
    for i, key in enumerate(faq_keys):
        if cols[i % 3].button(key.capitalize()):
            # Insert FAQ question into input box by setting session state
            st.session_state.user_input = key

    # Chat input at the top with send button
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    input_col, button_col = st.columns([8, 1])
    with input_col:
        user_input = st.text_input(
            "Ask me anything about rentals...",
            value=st.session_state.user_input,
            key="user_input",
            on_change=clear_input,
        )
    with button_col:
        send_clicked = st.button("Send")

    if send_clicked and st.session_state.user_input.strip() != "":
        prompt = st.session_state.user_input.strip()

        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Check for FAQ fallback
        lower_prompt = prompt.lower()
        faq_answer = None
        for key in base_faq_responses:
            if key in lower_prompt:
                faq_answer = base_faq_responses[key]
                break

        with st.chat_message("assistant"):
            if faq_answer:
                st.markdown(faq_answer)
                st.session_state.messages.append({"role": "assistant", "content": faq_answer})
            else:
                # Generate dynamic base prompt with live property data
                property_data_text = get_property_data_text()
                base_prompt = f"Hello, I am a rental assistant chatbot. Based on these data: {property_data_text}. Please answer briefly and to the point. If you don't know the answer, say: Sorry, I didn't understand the query. Please contact renters@gmail.com for further information. Previous conversation: "
                final_prompt = base_prompt + prompt
                response = ""
                for word in bot_response(final_prompt):
                    response += word
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat messages below input
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
