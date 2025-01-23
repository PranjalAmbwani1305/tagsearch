import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch article links based on a keyword
def fetch_article_links(keyword):
    base_url = "https://www.gujarat-samachar.com"  # Hardcoded URL
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links where the anchor text contains the keyword
        links = [a['href'] for a in soup.find_all('a', href=True) if keyword.lower() in a.text.lower()]
        return links, base_url
    except Exception as e:
        st.error(f"An error occurred while fetching links: {e}")
        return [], base_url

# Function to extract article content from a link
def extract_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract article content based on structure (e.g., <p> tags)
        paragraphs = soup.find_all('p')  # Adjust if needed for the website
        article_text = "\n".join(p.get_text() for p in paragraphs)
        return article_text if article_text else "No article content found."
    except Exception as e:
        return f"Error extracting article: {e}"

# Main Streamlit app
def main():
    st.title("Gujarati News Article Scraper")
    st.write("Enter a keyword to find articles and extract their content dynamically.")

    # Input field for the keyword
    keyword = st.text_input("Keyword to Search (Any)", "ટેકનોલોજી")  # Default: "Technology" in Gujarati

    if st.button("Find and Extract Articles"):
        if keyword:
            with st.spinner("Searching for articles..."):
                links, base_url = fetch_article_links(keyword)

                if links:
                    st.success(f"Found {len(links)} articles with the keyword '{keyword}':")
                    for link in links:
                        if not link.startswith("http"):  # Handle relative links
                            link = f"{base_url.rstrip('/')}/{link.lstrip('/')}"
                        st.write(f"**Link**: {link}")
                        with st.spinner("Extracting article content..."):
                            article_content = extract_article(link)
                            st.write(f"**Article Content**:\n{article_content}")
                else:
                    st.warning(f"No articles found with the keyword '{keyword}'.")
        else:
            st.error("Please enter a keyword.")

if __name__ == "__main__":
    main()
