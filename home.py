import streamlit as st
import pandas as pd
import database
import notifications

def app():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Renters Property Rental App</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Find your perfect rental property with ease</p>", unsafe_allow_html=True)

    # Sidebar with custom styling header
    st.sidebar.markdown("<h2 style='color: #4CAF50; border-bottom: 2px solid #4CAF50;'>Search Filters</h2>", unsafe_allow_html=True)

    # Fetch unique locations from database
    properties = database.get_properties()
    locations = list(set([prop[2] for prop in properties]))
    location_filter = st.sidebar.selectbox("Select Location", locations)

    max_rent = st.sidebar.slider("Max Rent (INR)", min_value=3000, max_value=20000, value=15000)

    # Fetch filtered properties from database
    filtered_properties = database.get_properties(location_filter, max_rent)

    if not filtered_properties:
        st.markdown("<h3 style='color: red;'>No Listings Found</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: #4CAF50;'>Available Listings</h3>", unsafe_allow_html=True)
        # Convert to DataFrame for display
        df = pd.DataFrame(filtered_properties, columns=["ID", "Property Name", "Location", "Rent (INR)", "Duration", "Owner Contact"])
        st.dataframe(df.style.set_properties(**{'background-color': '#f0f0f0', 'color': '#333', 'border': '1px solid #ddd'}))

    # Booking Request Form with a stylish form
    st.markdown("<h3 style='color: #4CAF50;'>Book a Property</h3>", unsafe_allow_html=True)

    if filtered_properties:
        property_names = [prop[1] for prop in filtered_properties]
        selected_property_name = st.selectbox("Choose a Property", property_names)
        name = st.text_input("Your Name", placeholder="Enter your full name")
        email = st.text_input("Your Email", placeholder="Enter your email address")
        if st.button("Submit Request"):
            # Find property id and owner email
            property_id = None
            owner_email = None
            for prop in filtered_properties:
                if prop[1] == selected_property_name:
                    property_id = prop[0]
                    owner_email = prop[5]
                    break
            if property_id and name and email:
                database.insert_booking(property_id, name, email)
                st.success(f"Booking request sent for {selected_property_name}. The owner will contact you soon!")
                # Send notification emails
                try:
                    notifications.send_booking_notification(email, selected_property_name, owner_email)
                except Exception as e:
                    st.error(f"Failed to send notification emails: {e}")
            else:
                st.error("Please fill all fields to submit booking request.")
    else:
        st.info("Please select a location and rent to see available properties and book.")

    # Review & Rating Section
    st.markdown("<h3 style='color: #4CAF50;'>Leave a Review</h3>", unsafe_allow_html=True)
    if filtered_properties:
        review_property_names = [prop[1] for prop in filtered_properties]
        selected_review_property_name = st.selectbox("Select Property to Review", review_property_names)
        review_text = st.text_area("Write your feedback", placeholder="Your thoughts...")
        rating = st.slider("Rate out of 5", 1, 5, 3)
        if st.button("Submit Review"):
            if review_text:
                # Find property id for review
                review_property_id = None
                for prop in filtered_properties:
                    if prop[1] == selected_review_property_name:
                        review_property_id = prop[0]
                        break
                if review_property_id is not None:
                    database.insert_review(review_property_id, review_text, rating)
                    st.success("Review submitted successfully!")
                else:
                    st.error("Selected property not found.")
            else:
                st.error("Please write a review before submitting.")
    else:
        st.info("Please select a location and rent to see available properties and leave a review.")

