import streamlit as st
import feedparser
# Set page title
# st.title("LEGIT NEWS")
st.write("<h1 style='text-align: center; font-size: 70px; color: #028d99;'>LEGIT NEWS</h1>", unsafe_allow_html=True)

# Define custom background styles
page_bg_img = '''
<style>
[data-testid="stSidebarContent"]{
    background: linear-gradient(0deg, #588EAD 0%, #151414 100%);   
}
.reportview-container {
    background: url("https://images.unsplash.com/photo-1487147264018-f937fba0c817");
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
# Function to parse RSS feed and display news
def rss_feed_url(url):
    rss_feed_contents = feedparser.parse(url)
    news = rss_feed_contents.entries
    
    for idx, curr_news in enumerate(news):
        id = str(idx+1)
        title = curr_news['title']
        actual_link = curr_news['link']
        content = curr_news['summary'].split('<')[0] if curr_news['summary'].split('<')[0] != '' else 'No article summary available, click on the link to read'

        st.header(f"\n({id}) {title}")
        st.write(f"{content}")
        st.write(f"Read full story here: {actual_link}")
        st.write("---------------------------------------------------------")

        if idx > 10:
            break

# Define button labels and corresponding RSS feed URLs
button_labels = ['Criminal law studies', 'India Legal Live', 'Indian Kanoon Latest Judgements', 'Judgements - Chennai']
feed_urls = ['https://criminallawstudiesnluj.wordpress.com/feed/',
             'https://www.indialegallive.com/feed',
             'https://indiankanoon.org/feeds/latest/judgments/',
             'https://indiankanoon.org/feeds/latest/chennai/']

# Display buttons in the sidebar
st.sidebar.title("News Stream Selector👇🏻")
selected_feed = st.sidebar.selectbox("", button_labels)
# Determine the selected feed and display news accordingly
for i, label in enumerate(button_labels):
    if selected_feed == label:
        st.title(f"{label}:\n")
        rss_feed_url(feed_urls[i])
