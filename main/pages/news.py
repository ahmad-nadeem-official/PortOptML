import feedparser
import streamlit as st


st.set_page_config(layout="wide")
st.title("Latest News about your favorite stocks")

ticker = "AAPL"
url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
feed = feedparser.parse(url)

for entry in feed.entries[:10]:
    title = entry.title
    link = entry.link
    
    # Some feeds include image in media_content or media_thumbnail
    image = None
    if "media_content" in entry:
        image = entry.media_content[0]['url']
    elif "media_thumbnail" in entry:
        image = entry.media_thumbnail[0]['url']
    
    st.write(title)
    st.write("Link:", link)
    st.write("Image:", image)
    st.write("-" * 50)