import streamlit as st
import json
import requests  
import streamlit as st 
from streamlit_lottie import st_lottie  

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
lottie_coding = load_lottiefile("Animation - news.json")

lottie_hello = load_lottieurl("https://lottie.host/e8ca8e9c-9297-4713-a89a-07e8da9522b8/iFSQ1Ui8v8.json")
lottie_hello1 = load_lottieurl("https://lottie.host/9fcb9eb8-21f7-41eb-8028-3d1fd309ea47/RQKh7FGAms.json")

page_bg_img = '''
<style>

[data-testid="stSidebarContent"]{
    background: linear-gradient(0deg, #588EAD 0%, #151414 100%);   
    }
# [data-testid="stAppViewContainer"]{
#     background: #ffffff url(https://cdn.pixabay.com/photo/2016/10/18/21/22/beach-1751455_1280.jpg) center center/cover no-repeat;
#     }
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)



def main():
    # st.title("LEGIT INSIGHTS")
    st.write("<h1 style='text-align: center; font-size: 80px; color: #028d99; font-family: Courier;'>LEGIT INSIGHTS</h1>", unsafe_allow_html=True)


    st.text("\n")
    st.write("<h1 style='text-align: center; font-size: 20px; color: #a7f4fa;'>Welcome to Legit Insights, your one-stop destination for all your legal needs. Here's what sets us apart:</h1>", unsafe_allow_html=True)

    st.text("\n")

    col1, col2 = st.columns([1, 2])

    with col1:

        st.write("News Updates: Stay ahead of the curve with our real-time news updates. Access timely and relevant information on legal matters, legislative changes, and industry trends, ensuring you're always informed and empowered to make informed decisions. From pivotal court rulings to game-changing policy shifts, empower yourself with the latest insights. Dive deep into critical legal developments and emerging industry trends, equipping yourself with the knowledge needed to navigate complex landscapes and anticipate future challenges. ")
    with col2:
            st_lottie(
        lottie_coding,
        speed=1,
        reverse=False,
        loop=True,
        quality="medium",
        # renderer="svg",
        height=None,
        width=None,
        key=None,
    )

        # st.image('C:\FYP1\LegitInsights\legalnews.jpg', caption='LEGIT NEWS', use_column_width=True)
    st.text("\n")

    col1, col2 = st.columns([1, 2])

    with col2:
        st.write("Chatbot Assistance (AstraPrime & Extracta): Need immediate legal guidance? Our chatbot feature provides personalized assistance round-the-clock. Get answers to your queries, receive tailored advice, and navigate legal complexities with ease, all through intuitive conversational interactions. Say goodbye to waiting rooms and hello to immediate guidance—empower yourself with intuitive conversations.")
    with col1:
        st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="medium",
        # renderer="svg",
        height=176,
        width=222,
        key=None,
        )
        # st.image('C:\FYP1\LegitInsights\chatbot.jpg', caption='LEGIT BOT', use_column_width=True)
    st.text("\n")

    col1, col2 = st.columns([1, 2])
    
    with col1:

        st.write("Legit Community: Join our vibrant community of users, where you can interact with peers, seek advice from experts, and share your experiences. Benefit from the collective wisdom of the crowd and gain valuable insights into various legal issues. Engage with articles covering diverse legal topics, stay informed on recent developments, and empower yourself with knowledge that matters.")
    with col2:
        st_lottie(
        lottie_hello1,
        speed=1,
        reverse=False,
        loop=True,
        quality="medium",
        # renderer="svg",
        height=330,
        width=450,
        key=None,
        )
        # st.image('C:\FYP1\LegitInsights\community.jpg', caption='LEGIT COMMUNITY', use_column_width=True)
    st.text("\n")

    st.write("At Legit Insights, we're committed to empowering individuals and businesses with convenient, accessible, and reliable legal assistance. Join us today and experience the future of legal services.")
    st.text("\n")
    st.write("Use the sidebar to navigate to different features of Legit Insights.")

    

    if st.button("FEATURED"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
