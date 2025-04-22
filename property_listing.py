import streamlit as st
import database
import notifications

def app():
    st.title("Property Listings")

    # Filters
    location_filter = st.text_input("Filter by Location")
    max_rent_filter = st.number_input("Max Rent", min_value=0, step=1000)

    # Fetch properties with filters
    properties = database.get_properties(
        location=location_filter if location_filter else None,
        max_rent=max_rent_filter if max_rent_filter > 0 else None
    )

    if not properties:
        st.write("No properties found with the given filters.")
        return

    for prop in properties:
        prop_id, name, location, rent, duration, owner_contact = prop
        st.subheader(name)
        st.write(f"Location: {location}")
        st.write(f"Rent: {rent}")
        st.write(f"Duration: {duration}")
        st.write(f"Owner Contact: {owner_contact}")

        if 'logged_in' in st.session_state and st.session_state.logged_in:
            with st.form(f"booking_form_{prop_id}"):
                st.write("Book this property")
                user_name = st.text_input("Your Name", key=f"name_{prop_id}")
                user_email = st.text_input("Your Email", key=f"email_{prop_id}")
                submitted = st.form_submit_button("Book Now")
                if submitted:
                    if user_name and user_email:
                        database.insert_booking(prop_id, user_name, user_email)
                        notifications.send_booking_notification(user_email, name, owner_contact)
                        st.success("Booking successful! Notification emails sent.")
                    else:
                        st.error("Please enter your name and email to book.")
        else:
            st.info("Please login to book a property.")
