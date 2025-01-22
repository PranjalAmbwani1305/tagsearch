import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_article_by_keyword(search_keyword):
    # Construct the search URL
    url = f"https://www.gujaratsamachar.com/search?search={search_keyword}"
    
    # Send a GET request
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find articles (adjust class name based on actual HTML structure)
        articles = soup.find_all('div', class_='article')  # Adjust this based on the actual HTML structure
        
        # Check if any articles were found
        if articles:
            # Extract the first article
            first_article = articles[0]
            title = first_article.find('h2').text.strip()  # Adjust based on actual HTML structure
            link = first_article.find('a')['href']  # Adjust based on actual HTML structure
            
            return title, link
        else:
            return None, None
    else:
        return None, None

# Streamlit application
st.title("Gujarat Samachar Article Search")

# Input field for the search keyword
search_keyword = st.text_input("Enter a keyword to search for articles:")

if st.button("Search"):
    if search_keyword:
        title, link = scrape_article_by_keyword(search_keyword)
        
        if title and link:
            st.success("Article found!")
            st.write(f"**Title:** {title}")
            st.write(f"[Read more]({link})")
        else:
            st.error("No articles found for the given keyword.")
    else:
        st.warning("Please enter a keyword to search.")
