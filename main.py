import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch article links based on a search tag
def fetch_article_links(base_url, search_tag):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Adjust this selector based on Gujarat Samachar's HTML structure
        links = [a['href'] for a in soup.find_all('a', href=True) if search_tag in a.text]
        return links
    except Exception as e:
        st.error(f"An error occurred while fetching links: {e}")
        return []

# Function to extract article content from a link
def extract_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Adjust this to select the main content based on Gujarat Samachar's structure
        paragraphs = soup.find_all('p')  # Find all <p> tags that contain article text
        article_text = "\n".join(p.get_text() for p in paragraphs)  # Combine paragraph text
        return article_text if article_text else "No article content found."
    except Exception as e:
        return f"Error extracting article: {e}"

# Main Streamlit app
def main():
    st.title("Gujarat Samachar Article Extractor")
    st.write("Enter the Gujarat Samachar website URL and a keyword to find articles and extract their content.")

    # Input fields for URL and search tag
    base_url = st.text_input("Gujarat Samachar Website URL", "https://www.gujarat-samachar.com")
    search_tag = st.text_input("Gujarati Keyword to Search", "સમાચાર")  # Default: "news" in Gujarati

    if st.button("Find and Extract Articles"):
        if base_url and search_tag:
            with st.spinner("Searching for articles..."):
                links = fetch_article_links(base_url, search_tag)

                if links:
                    st.success(f"Found {len(links)} articles with the keyword '{search_tag}':")
                    for link in links:
                        if not link.startswith("http"):  # Handle relative links
                            link = f"{base_url.rstrip('/')}/{link.lstrip('/')}"
                        st.write(f"**Link**: {link}")
                        with st.spinner("Extracting article content..."):
                            article_content = extract_article(link)
                            st.write(f"**Article Content**:\n{article_content}")
                else:
                    st.warning("No articles found with the specified keyword.")
        else:
            st.error("Please enter both a website URL and a keyword.")

if __name__ == "__main__":
    main()
