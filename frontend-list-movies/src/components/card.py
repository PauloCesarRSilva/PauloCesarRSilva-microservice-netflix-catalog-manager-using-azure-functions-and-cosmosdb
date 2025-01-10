def VideoCard(id, title, thumbnail, video_url):
    import streamlit as st

    # Create a card layout
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(thumbnail, use_container_width=True)
        
        with col2:
            st.subheader(title)
            if st.button("Play Video", key=id):
                st.video(video_url)