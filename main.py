import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Fetch article links based on keyword
def fetch_article_links(base_url, keyword):
    try:
        response = requests.get(base_url, timeout=10)
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
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while fetching links: {e}")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []

# Extract article content and publication date
def extract_article(link):
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt to extract publication date
        date = soup.find('h5')  # Adjust the tag based on the actual structure of the site
        article_date = date.get_text(strip=True) if date else "Date not found"

        # Attempt to extract article content
        content = soup.find('div', class_='article-body')  # Adjust selector as needed
        if content:
            article_text = "\n".join(p.get_text() for p in content.find_all('p'))
        else:
            paragraphs = soup.find_all('p')
            article_text = "\n".join(p.get_text() for p in paragraphs if p.get_text())

        return article_date, article_text if article_text else "No article content found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching article: {e}", ""
    except Exception as e:
        return f"Error extracting article content: {e}", ""

# Translate text to the target language
def translate_text(text, target_language="en"):
    try:
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated
    except Exception as e:
        st.error(f"Error translating article: {e}")
        return text

# Main Streamlit application
def main():
    st.set_page_config(page_title="Gujarati News Article Scraper", page_icon="📰")
    st.title("Gujarati News Article Finder")

    # Define the base URL
    base_url = "https://www.gujarat-samachar.com/"

    # User input for keyword
    keyword = st.text_input("Keyword to Search")

    # Search for articles when the button is clicked
    if st.button("Find and Extract Articles"):
        if keyword:
            with st.spinner("Searching for articles..."):
                links = fetch_article_links(base_url, keyword)

                if links:
                    st.success(f"Found {len(links)} articles with the keyword '{keyword}':")
                    for i, link in enumerate(links, start=1):
                        st.write(f"**Article {i}:** [Link]({link})")
                        with st.spinner("Extracting article content..."):
                            article_date, article_content = extract_article(link)
                            st.write(f"**Published on:** {article_date}")

                            if article_content:
                                st.write(f"**Article Content (Original):**\n{article_content[:500]}...")  # Show part of the article
                                translated_content = translate_text(article_content, target_language="en")
                                st.write(f"**Article Content (Translated to English):**\n{translated_content[:500]}...")
                            else:
                                st.warning(f"Article {i} has no content.")
                else:
                    st.warning(f"No articles found with the keyword '{keyword}'.")
        else:
            st.error("Please enter a keyword.")

if __name__ == "__main__":
    main()
