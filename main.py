import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch article links based on any keyword
def fetch_article_links(base_url, keyword):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links where the anchor text contains the keyword
        links = []
        for a in soup.find_all('a', href=True):
            if keyword.lower() in a.text.lower():
                href = a['href']
                # Handle relative URLs
                if not href.startswith("http"):
                    href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
                links.append(href)

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

        # Extract article content based on structure (e.g., <p> tags)
        paragraphs = soup.find_all('p')  # Adjust if needed for the specific website
        article_text = "\n".join(p.get_text() for p in paragraphs if p.get_text())
        return article_text if article_text else "No article content found."
    except Exception as e:
        return f"Error extracting article: {e}"

# Main Streamlit app
def main():
    st.title("Gujarati News Article Scraper")
    st.write("Enter a Gujarati news website URL and a keyword to find articles and extract their content dynamically.")

    # Input fields for URL and keyword
    base_url = st.text_input("Gujarati News Website URL", "https://www.gujarat-samachar.com")
    keyword = st.text_input("Keyword to Search (Any)", "ટેકનોલોજી")  # Default: "Technology" in Gujarati

    if st.button("Find and Extract Articles"):
        if base_url and keyword:
            with st.spinner("Searching for articles..."):
                links = fetch_article_links(base_url, keyword)

                if links:
                    st.success(f"Found {len(links)} articles with the keyword '{keyword}':")
                    for i, link in enumerate(links, start=1):
                        st.write(f"**Article {i}:** [Link]({link})")
                        with st.spinner("Extracting article content..."):
                            article_content = extract_article(link)
                            st.write(f"**Article Content:**\n{article_content}\n")
                else:
                    st.warning(f"No articles found with the keyword '{keyword}'.")
        else:
            st.error("Please enter both a website URL and a keyword.")

if __name__ == "__main__":
    main()
