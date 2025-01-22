import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit title
st.title('Gujarati Newspaper Web Scraping')

url = 'https://www.gujaratsamachar.com/'  
st.write(f"Scraping content from: {url}")

try:
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    response.encoding = 'utf-8'  # Ensure Gujarati characters are properly decoded
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tag = st.text_input('Enter the tag to search for (e.g., h1, p):', 'h1')

    if tag:
        elements = soup.find_all(tag)
        if elements:
            st.write(f"Found {len(elements)} <{tag}> elements:")
            for element in elements:
                st.write(element.text)  # Display the text of each found element
        else:
            st.write(f"No <{tag}> tags found.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching the URL: {e}")
