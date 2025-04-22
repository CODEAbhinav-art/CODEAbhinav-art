import streamlit as st

def app():
    st.markdown(
        """
        <style>
        /* Amazon-like dark background with animated orange gradient */
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            background: linear-gradient(270deg, #131921, #FF9900, #FF6F00, #131921);
            background-size: 800% 800%;
            animation: gradientAnimation 15s ease infinite;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            color: white;
            cursor: url('https://cdn-icons-png.flaticon.com/512/32/32339.png'), auto;
        }

        @keyframes gradientAnimation {
            0%{background-position:0% 50%}
            50%{background-position:100% 50%}
            100%{background-position:0% 50%}
        }

        .content-container {
            max-width: 900px;
            margin: 40px auto;
            padding: 20px 40px;
            background: rgba(0,0,0,0.7); /* Slightly transparent black background for content */
            border-radius: 12px;
            box-shadow: 0 0 30px rgba(255, 153, 0, 0.7); /* Orange glow shadow */
        }
        h1, h2 {
            font-weight: 900;
            letter-spacing: 1.5px;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            color: #FF9900; /* Amazon orange */
            text-align: center;
        }
        h2 {
            font-size: 2rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #FFB84D; /* lighter orange */
        }
        p {
            font-size: 1.125rem;
            line-height: 1.6;
            color: #f0f0f0;
            text-align: center;
        }
        ul {
            list-style: none;
            padding-left: 0;
            color: #f5f5f5;
            font-size: 1rem;
        }
        ul li {
            margin-bottom: 0.75rem;
            position: relative;
            padding-left: 1.5rem;
        }
        ul li::before {
            content: "✔";
            position: absolute;
            left: 0;
            color: #FF9900;
            font-weight: bold;
        }
        .footer {
            margin-top: 40px;
            font-size: 0.9rem;
            color: #ccc;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown("<h1>Renters</h1>", unsafe_allow_html=True)
    st.markdown("<h1>About Renters Property Rental App</h1>", unsafe_allow_html=True)
    st.markdown("<p>Your one-stop solution to find and book rental properties with ease.</p>", unsafe_allow_html=True)

    with st.expander("Features", expanded=False):
        st.markdown(
            """
            <ul>
                <li>Search rental properties by location and budget</li>
                <li>View detailed listings with contact information</li>
                <li>Book properties directly through the app</li>
                <li>Leave reviews and ratings for properties</li>
                <li>Persistent data storage using SQLite</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Technology Stack", expanded=False):
        st.markdown(
            """
            <ul>
                <li>Python and Streamlit for the web app</li>
                <li>SQLite for database management</li>
                <li>HTML, CSS, and Lottie animations for UI enhancements</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<p class="footer">Thank you for using Renters Property Rental App!</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
