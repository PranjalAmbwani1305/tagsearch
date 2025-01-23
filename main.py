import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def translate_keyword_to_gujarati(keyword):
    try:
        translated = GoogleTranslator(source='en', target='gu').translate(keyword)
        return translated
    except Exception as e:
        st.error(f"Error translating keyword: {e}")
        return keyword

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
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while fetching links: {e}")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []

def extract_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        date = soup.find('h5')
        article_date = date.get_text(strip=True) if date else "Date not found"

        content = soup.find('div', class_='article-body')
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

def main():
    st.set_page_config(page_title="Gujarati News Article Scraper", page_icon="📰")
    st.title("Gujarati News Article Finder")

    base_url = "https://www.gujarat-samachar.com/"
    keyword = st.text_input("Keyword to Search (English or Gujarati)")

    if keyword:
        if not any(ord(char) > 128 for char in keyword):
            translated_keyword = translate_keyword_to_gujarati(keyword)
            st.write(f"Translated keyword (Gujarati): {translated_keyword}")
        else:
            translated_keyword = keyword
            st.write(f"Using entered Gujarati keyword: {translated_keyword}")

    if st.button("Find and Extract Articles"):
        if keyword:
            with st.spinner("Searching for articles..."):
                links = fetch_article_links(base_url, translated_keyword)

                if links:
                    st.success(f"Found {len(links)} articles with the keyword '{keyword}':")
                    for i, link in enumerate(links, start=1):
                        st.write(f"**Article {i}:** [Link]({link})")
                        with st.spinner("Extracting article content..."):
                            article_date, article_content = extract_article(link)
                            st.write(f"**Published on:** {article_date}")

                            if article_content:
                                st.write(f"**Article Content:**\n{article_content}")
                            else:
                                st.warning(f"Article {i} has no content.")
                else:
                    st.warning(f"No articles found with the keyword '{keyword}'.")
        else:
            st.error("Please enter a keyword.")

if __name__ == "__main__":
    main()
