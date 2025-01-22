import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit title
st.title('Gujarati Newspaper Web Scraping')

url = 'https://www.gujaratsamachar.com/'  
st.write(f"Scraping content from: {url}")

try:
    response = requests.get(url)
    response.raise_for_status()  
    response.encoding = 'utf-8'  
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tag = st.text_input('Enter the tag to search for ','h1')

    if tag:
        elements = soup.find_all(tag)
        if elements:
            st.write(f"Found {len(elements)} <{tag}> elements:")
            for element in elements:
                st.write(element.text)  
        else:
            st.write(f"No <{tag}> tags found.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching the URL: {e}")
