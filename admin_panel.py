import streamlit as st
import database

ADMIN_PASSWORD = "admin123"  # Simple password for admin access

def app():
    st.title("Admin Panel")

    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password = st.text_input("Enter admin password", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Logged in as admin")
            else:
                st.error("Incorrect password")
        return

    st.subheader("Add New Property")
    with st.form("add_property_form"):
        name = st.text_input("Property Name")
        location = st.text_input("Location")
        rent = st.number_input("Rent", min_value=0)
        duration = st.text_input("Duration")
        owner_contact = st.text_input("Owner Contact Email")
        submitted = st.form_submit_button("Add Property")
        if submitted:
            if name and location and rent and duration and owner_contact:
                conn = database.create_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO properties (name, location, rent, duration, owner_contact) VALUES (?, ?, ?, ?, ?)",
                    (name, location, rent, duration, owner_contact)
                )
                conn.commit()
                conn.close()
                st.success("Property added successfully")
            else:
                st.error("Please fill all fields")

    st.subheader("Manage Properties")
    properties = database.get_properties()
    for prop in properties:
        prop_id, name, location, rent, duration, owner_contact = prop
        st.write(f"ID: {prop_id} | Name: {name} | Location: {location} | Rent: {rent} | Duration: {duration} | Owner: {owner_contact}")
        if st.button(f"Delete Property {prop_id}"):
            conn = database.create_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM properties WHERE id = ?", (prop_id,))
            conn.commit()
            conn.close()
            st.success(f"Property {prop_id} deleted")
            st.experimental_rerun()
