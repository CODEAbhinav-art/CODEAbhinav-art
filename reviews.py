import streamlit as st
import database

def app():
    st.title("Leave a Review")

    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("Please login to leave a review.")
        return

    properties = database.get_properties()
    property_dict = {prop[0]: prop[1] for prop in properties}  # id: name

    selected_property_id = st.selectbox("Select Property to Review", options=list(property_dict.keys()), format_func=lambda x: property_dict[x])

    review_text = st.text_area("Write your review here")
    rating = st.slider("Rating", min_value=1, max_value=5, value=3)

    if st.button("Submit Review"):
        if review_text:
            database.insert_review(selected_property_id, review_text, rating)
            st.success("Thank you for your review!")
        else:
            st.error("Please write a review before submitting.")

    st.subheader("Reviews")

    # Display reviews grouped by property
    for prop_id, prop_name in property_dict.items():
        st.write(f"### {prop_name}")
        reviews = get_reviews_by_property(prop_id)
        if reviews:
            avg_rating = sum([r['rating'] for r in reviews]) / len(reviews)
            st.write(f"Average Rating: {avg_rating:.1f} / 5")
            for review in reviews:
                st.write(f"- {review['review_text']} (Rating: {review['rating']})")
        else:
            st.write("No reviews yet.")

def get_reviews_by_property(property_id):
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT review_text, rating FROM reviews WHERE property_id = ?", (property_id,))
    rows = cursor.fetchall()
    conn.close()
    reviews = []
    for row in rows:
        reviews.append({
            "review_text": row[0],
            "rating": row[1]
        })
    return reviews
