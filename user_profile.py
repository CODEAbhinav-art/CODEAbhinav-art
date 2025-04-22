import streamlit as st
import database

def app():
    st.title("User Profile")

    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("Please login to view your profile.")
        return

    user_email = st.session_state.user['email']
    st.write(f"Logged in as: {user_email}")

    # Display user booking history
    st.subheader("Your Bookings")
    bookings = get_user_bookings(user_email)
    if bookings:
        for booking in bookings:
            booking_id = booking['id']
            st.write(f"Property: {booking['property_name']}")
            st.write(f"Location: {booking['location']}")
            st.write(f"Rent: {booking['rent']}")
            st.write(f"Duration: {booking['duration']}")
            if st.button(f"Cancel Booking {booking_id}"):
                database.cancel_booking(booking_id)
                st.success("Booking cancelled successfully.")
                st.experimental_rerun()
            st.write("---")
    else:
        st.write("You have no bookings.")

def get_user_bookings(email):
    conn = database.create_connection()
    cursor = conn.cursor()
    query = """
    SELECT b.id, p.name, p.location, p.rent, p.duration
    FROM bookings b
    JOIN properties p ON b.property_id = p.id
    WHERE b.email = ?
    """
    cursor.execute(query, (email,))
    rows = cursor.fetchall()
    conn.close()
    bookings = []
    for row in rows:
        bookings.append({
            "id": row[0],
            "property_name": row[1],
            "location": row[2],
            "rent": row[3],
            "duration": row[4]
        })
    return bookings
