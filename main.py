import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title('Search Articles by Keyword')

url = 'https://www.gujaratsamachar.com/'
st.write(f"Scraping content from: {url}")

search_word = st.text_input('Enter a word to search for related articles:')

if search_word:
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')

        found_articles = []

        all_elements = soup.find_all(text=True)  # Get all textual content

        for element in all_elements:
            if search_word.lower() in element.lower():
                found_articles.append(element.strip())

        if found_articles:
            st.write(f"Found {len(found_articles)} articles related to '{search_word}':")
            for article in found_articles:
                st.write(f"- {article}")
        else:
            st.write(f"No articles found related to '{search_word}'.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
