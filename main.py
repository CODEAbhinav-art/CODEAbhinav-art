import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import about,account,chatbot,home

st.set_page_config(page_title="Rental House", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

class MultiPage:
    
    def __init__(self):
        self.apps = []
        
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
        
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title="renters",
                options=["home", "about", "account", "chatbot"],
                icons=["🏠", "📄", "👤", "🤖"],
                menu_icon="chat-text-fill",
                default_index=1,
                styles={"menu_icon_style": "background-color: #f5f5f5; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"})


        if app == "home":
            home.app()
        elif app == "about":
            about.app()
        elif app == "account":
            account.app()
        elif app == "chatbot":
            chatbot.app()
           
    run()       
    
# Sample data for listings
data = {
    "Property Name": ["Student PG in Vadodara", "1BHK near MSU", "Shared Hostel Room", "2BHK Apartment", "Studio Apartment"],
    "Location": ["Vadodara", "Vadodara", "Mumbai", "Ahmedabad", "Vadodara"],
    "Rent (INR)": [6000, 12000, 5000, 18000, 8000],
    "Duration": ["1 Month", "3 Months", "6 Months", "12 Months", "3 Months"],
    "Owner Contact": ["ramesh_rentals@gmail.com", "Kishan_houses@gmail.com", "satyam_pgs@gmail.com", "vijay.rentals@example.com", "info@modernliving.in"]
}
df = pd.DataFrame(data)

# Sidebar with custom styling header
st.sidebar.markdown("<h2 style='color: #4CAF50;'>Search Filters</h2>", unsafe_allow_html=True)
location_filter = st.sidebar.selectbox("Select Location", df["Location"].unique())
max_rent = st.sidebar.slider("Max Rent (INR)", min_value=3000, max_value=20000, value=15000)

# Filtered Results
filtered_df = df[(df["Location"] == location_filter) & (df["Rent (INR)"] <= max_rent)]

if filtered_df.empty:
    st.markdown("<h3>No Listings Found</h3>", unsafe_allow_html=True)
else:
    st.markdown("<h3>Available Listings</h3>", unsafe_allow_html=True)
    st.table(filtered_df)

# Booking Request Form with a stylish form
st.markdown("<h3>Book a Property</h3>", unsafe_allow_html=True)

if not filtered_df.empty:
    selected_property = st.selectbox("Choose a Property", filtered_df["Property Name"])
    name = st.text_input("Your Name", placeholder="Enter your full name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    if st.button("Submit Request"):
        st.success(f"Booking request sent for {selected_property}. The owner will contact you soon!")
else:
    st.write("Please select a location and rent to see available properties and book.")

# Review & Rating Section
st.markdown("<h3>Leave a Review</h3>", unsafe_allow_html=True)
review_text = st.text_area("Write your feedback", placeholder="Your thoughts...")
rating = st.slider("Rate out of 5", 1, 5, 3)
if st.button("Submit Review"):
    st.success("Review submitted successfully!")

