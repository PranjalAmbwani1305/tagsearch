import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_article_links(base_url, keyword):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        for a in soup.find_all('a', href=True):
            if keyword.lower() in a.text.lower():
                href = a['href']
                if not href.startswith("http"):
                    href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"

                links.append(href)

        return links
    except Exception as e:
        st.error(f"An error occurred while fetching links: {e}")
        return []

def extract_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        article_text = "\n".join(p.get_text() for p in paragraphs if p.get_text())
        return article_text if article_text else "No article content found."
    except Exception as e:
        return f"Error extracting article: {e}"

def main():
    st.set_page_config(page_title="Gujarati News Article Scraper", page_icon="📚")
    
    st.title("Gujarati News Article Scraper")
    st.write("Search for articles on **Gujarat Samachar** using a keyword and extract their content dynamically.")

    base_url = "https://www.gujarat-samachar.com/"

    keyword = st.text_input("Enter a Keyword to Search", "ટેકનોલોજી")

    if st.button("Find and Extract Articles"):
        if keyword:
            with st.spinner("Searching for articles..."):
                links = fetch_article_links(base_url, keyword)

                if links:
                    st.success(f"Found {len(links)} articles with the keyword '{keyword}':")
                    for i, link in enumerate(links, start=1):
                        st.markdown(f"### Article {i}: [Click here to read]({link})")
                        with st.spinner("Extracting article content..."):
                            article_content = extract_article(link)
                            st.text_area(f"Article {i} Content:", article_content, height=300)
                else:
                    st.warning(f"No articles found with the keyword '{keyword}'.")
        else:
            st.error("Please enter a keyword.")

if __name__ == "__main__":
    main()
