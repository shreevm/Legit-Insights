import streamlit as st
from pages.Blog import main as blog_page
from pages.settings import main as settings_page
from pages.pro import main as profile_page
from pages.chatbot import main as chatbot_page
from home import main as home_page

# from news import main as news_page

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ("Home","Legit News", "Legit Bot", "Legit Community","Profile", "Settings"))

    if page == "Home":
        # st.title("Welcome to the Home Page")
        # st.write("This is the home page where you can navigate to different sections of the app.")
        # st.write("Use the sidebar to navigate to different pages.")
        home_page()
    
    elif page == "Legit Community":
        blog_page()

    elif page == "Settings":
        settings_page()

    elif page == "Profile":
        profile_page()

    elif page == "Legit Bot":
        chatbot_page()

    # elif page == "Legit News":
    #     news_page()

if __name__ == "__main__":
    main()
