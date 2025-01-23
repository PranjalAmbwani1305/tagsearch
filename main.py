import streamlit as st
import requests
from bs4 import BeautifulSoup

# Fetch article links and relevant text dynamically
def fetch_article_links(keyword):
    base_url = "https://www.gujarat-samachar.com"  # Hardcoded URL
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Debugging: Show raw HTML structure
        if st.checkbox("Show Page HTML (Debugging)"):
            st.text(soup.prettify())

        # Search across all tags for the keyword
        links = []
        for tag in soup.find_all(True):  # `True` matches all tags
            text = tag.get_text(strip=True)  # Extract visible text
            if keyword.lower() in text.lower():  # Match keyword
                if tag.name == "a" and tag.has_attr('href'):  # If it's a link
                    href = tag['href']
                    links.append(href)
        return links, base_url
    except Exception as e:
        st.error(f"An error occurred while fetching links: {e}")
        return [], base_url

# Extract content from an article link
def extract_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from all possible content tags
        content_tags = soup.find_all(['p', 'div', 'span'])  # Add tags as needed
        article_text = "\n".join(tag.get_text(strip=True) for tag in content_tags)
        return article_text if article_text else "No article content found."
    except Exception as e:
        return f"Error extracting article: {e}"

# Main Streamlit app
def main():
    st.title("Gujarati News Scraper")
    st.write("Enter a keyword to search articles and extract their content dynamically.")

    # Input field for the keyword
    keyword = st.text_input("Keyword to Search (Any)", "સમાચાર")  # Default: "News" in Gujarati

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
