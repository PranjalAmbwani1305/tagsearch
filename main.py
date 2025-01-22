import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title('Gujarati Newspaper Web Scraping')

url = 'https://www.gujaratsamachar.com/'  # Change this to the actual URL
st.write(f"Scraping content from: {url}")

tag = st.text_input('Enter the tag to search for (e.g., h1, p):', 'h1')

  
