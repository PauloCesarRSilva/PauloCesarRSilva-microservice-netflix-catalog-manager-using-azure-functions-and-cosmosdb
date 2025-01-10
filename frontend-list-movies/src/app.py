import streamlit as st
from utils.api import fetch_videos
from components.card import VideoCard

def main():
    st.title("Dio Flix")
    
    # Fetch video data from the API
    api = 'http://localhost:7071/funcGetDatabase'
    videos = fetch_videos(api)

    if videos:
        for video in videos['data']:
            VideoCard(id=video['id'], 
                      title=video['title'], 
                      thumbnail=video['thumb'], 
                      video_url=video['video'])
    else:
        st.write("No videos available.")

if __name__ == "__main__":
    main()