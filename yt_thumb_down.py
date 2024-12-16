import streamlit as st
import yt_dlp
import requests
from PIL import Image
from io import BytesIO

# Streamlit App Title
st.title("YouTube Thumbnail Downloader")
st.write("Paste a YouTube video link to view and download its thumbnail.")

# Input Text Box
video_url = st.text_input("Enter YouTube Video URL:")

if video_url:
    try:
        # Use yt-dlp to get video details
        ydl_opts = {
            'quiet': True,  # Suppresses unnecessary output
            'extract_flat': True,  # Skip downloading the video
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get("title", "No Title Available")
            thumbnail_url = info_dict.get("thumbnail", "")
        
        # Display Video Title
        st.subheader(f"Video Title: {video_title}")
        
        # Fetch and Display Thumbnail
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="YouTube Thumbnail", use_column_width=True)
                
                # Generate Download Button
                file_name = video_title.split()[0] + ".jpg"  # Use the first word of the title as the file name
                img_buffer = BytesIO()
                image.save(img_buffer, format="JPEG")
                img_buffer.seek(0)
                
                st.download_button(
                    label="Download Thumbnail",
                    data=img_buffer,
                    file_name=file_name,
                    mime="image/jpeg"
                )
            else:
                st.error("Failed to fetch the thumbnail image.")
        else:
            st.error("No thumbnail available.")
    
    except Exception as e:
        st.error(f"Error: {e}")
