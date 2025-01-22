import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to search articles on GujaratiSamachar Live website
def search_articles(search_term):
    url = "https://www.gujaratsamachar.com/"  # Replace with the live website URL
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error("Failed to retrieve the webpage.")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all article links (Adjust this based on the actual website's HTML structure)
    articles = soup.find_all('a', href=True)
    
    results = []
    
    # Check each article for the search term
    for article in articles:
        title = article.get_text().strip()
        link = article['href']
        
        if search_term.lower() in title.lower():
            results.append({'title': title, 'link': link})
    
    return results

# Streamlit App
def app():
    st.title("GujaratiSamachar Article Search")
    st.write("Enter a word or sentence to search for related articles.")
    
    search_term = st.text_input("Search Term:")
    
    if search_term:
        with st.spinner('Searching articles...'):
            found_articles = search_articles(search_term)
        
        if found_articles:
            st.write(f"Found {len(found_articles)} article(s):")
            for article in found_articles:
                st.write(f"**{article['title']}**")
                st.write(f"[Read more]({article['link']})")
        else:
            st.write("No articles found matching your search term.")
    else:
        st.write("Please enter a search term to begin.")

if __name__ == "__main__":
    app()
