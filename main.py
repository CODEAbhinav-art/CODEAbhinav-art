import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import about, account, chatbot, home, property_listing, reviews, user_profile, admin_panel

st.set_page_config(page_title="Rental House", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

class MultiPage:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        with st.sidebar:
            # Add custom CSS for option menu to enforce square buttons and gradient backgrounds
            st.markdown(
                """
                <style>
                /* Container gradient background */
                .sidebar .css-1d391kg {
                    background: linear-gradient(90deg, #FF6F00, #FF9900, #FF6F00) !important;
                    padding: 5px !important;
                    border-radius: 8px !important;
                }
                /* Option menu links */
                .streamlit-option-menu .nav-link {
                    border-radius: 8px !important;
                    color: white !important;
                    font-weight: 600 !important;
                    margin: 5px 0 !important;
                    padding: 10px 20px !important;
                    transition: all 0.3s ease !important;
                    background: transparent !important;
                    display: flex !important;
                    align-items: center !important;
                }
                /* Hover effect */
                .streamlit-option-menu .nav-link:hover {
                    background: linear-gradient(90deg, #FF9900, #FF6F00) !important;
                    color: white !important;
                }
                /* Selected link */
                .streamlit-option-menu .nav-link-selected {
                    background: linear-gradient(90deg, #FF6F00, #FF9900) !important;
                    color: white !important;
                    border-radius: 8px !important;
                }
                /* Icons */
                .streamlit-option-menu .nav-link .icon {
                    color: white !important;
                    font-size: 20px !important;
                    margin-right: 10px !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            
            app = option_menu(
                menu_title="RENTERS",
                options=["home", "about", "account", "chatbot", "property_listing", "reviews", "user_profile", "admin_panel"],
                icons=["🏠", "📄", "👤", "🤖", "🏘️", "⭐", "👤", "🔧"],
                menu_icon="chat-text-fill",
                default_index=1,
                styles={
                    "container": {
                        "padding": "5px",
                        "background": "transparent"
                    },
                    "icon": {
                        "color": "#FFFFFF",
                        "font-size": "20px",
                        "margin-left": "5px"
                    },
                    "nav-link": {
                        "border-radius": "8px",
                        "color": "#FFFFFF",
                        "font-weight": "600",
                        "margin": "5px 0",
                        "padding": "10px 20px",
                        "transition": "all 0.3s ease",
                        "background": "transparent",
                        "display": "flex",
                        "align-items": "center"
                    },
                    "nav-link:hover": {
                        "background": "linear-gradient(90deg, #FF9900, #FF6F00)",
                        "color": "#FFFFFF"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(90deg, #FF6F00, #FF9900)",
                        "color": "#FFFFFF",
                        "border-radius": "8px"
                    },
                    "menu-icon-style": {
                        "background-color": "#FF9900",
                        "border-radius": "8px",
                        "box-shadow": "0 2px 6px rgba(255, 153, 0, 0.7)"
                    }
                }
            )

        if app == "home":
            home.app()
        elif app == "about":
            about.app()
        elif app == "account":
            account.app()
        elif app == "chatbot":
            chatbot.app()
        elif app == "property_listing":
            property_listing.app()
        elif app == "reviews":
            reviews.app()
        elif app == "user_profile":
            user_profile.app()
        elif app == "admin_panel":
            admin_panel.app()

multi_page = MultiPage() #Create an instance of MultiPage.
multi_page.run() # call run method from the instance.
