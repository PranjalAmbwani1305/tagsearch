import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

def fetch_article_links_by_keyword(base_url, keyword, max_pages=5):
    try:
        links = []
        page = 1

        while page <= max_pages:
            url = f"{base_url}?page={page}" if page > 1 else base_url
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            for a in soup.find_all('a', href=True):
                if keyword.lower() in a.get('href', '').lower() or keyword.lower() in a.text.lower():
                    href = a['href']
                    if not href.startswith("http"):
                        href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"

                    links.append(href)

            next_page = soup.find('a', text='Next')
            if next_page:
                page += 1
            else:
                break

        return links
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        st.error(f"Oops! Something went wrong while fetching the links: {e}")
        return []

def fetch_article_links_by_date(base_url, date_str, max_pages=5):
    try:
        links = []
        page = 1

        while page <= max_pages:
            url = f"{base_url}?page={page}" if page > 1 else base_url
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            for a in soup.find_all('a', href=True):
                href = a['href']
                if date_str in href:
                    if not href.startswith("http"):
                        href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"

                    links.append(href)

            next_page = soup.find('a', text='Next')
            if next_page:
                page += 1
            else:
                break

        return links
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        st.error(f"Oops! Something went wrong while fetching the links: {e}")
        return []

def extract_article(link, newspaper):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        article_date = "Date not found"
        if newspaper == "Gujarat Samachar":
            date_element = soup.find('span', class_='post-date')
            if date_element:
                article_date = date_element.get_text(strip=True)

        article_text = ""
        content = None
        if newspaper == "Gujarat Samachar":
            content = soup.find('div', class_='td-post-content')

        if content:
            paragraphs = content.find_all('p')
            seen_text = set()
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text and text not in seen_text:
                    article_text += text + "\n"
                    seen_text.add(text)
        else:
            paragraphs = soup.find_all('p')
            seen_text = set()
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text and text not in seen_text:
                    article_text += text + "\n"
                    seen_text.add(text)

        return article_date, article_text.strip() if article_text else "No article content found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching article content: {e}", ""
    except Exception as e:
        return f"Error extracting article: {e}", ""

def main():
    st.set_page_config(page_title="Gujarati News Article Scraper", page_icon="📰")
    st.title("Gujarati News Article Finder")

    st.markdown("""
    **Welcome to the Gujarati News Article Finder!**
    This tool allows you to search for articles from popular Gujarati newspapers.
    You can search articles by a **keyword** or by a **specific date**.
    """)

    newspaper = "Gujarat Samachar"  # Default to Gujarat Samachar

    newspaper_urls = {
        "Gujarat Samachar": "https://www.gujaratsamachar.com/",
    }

    base_url = newspaper_urls.get(newspaper)

    # Choose search method
    search_method = st.selectbox("Choose search method", ("By Keyword", "By Date"))

    if search_method == "By Keyword":
        keyword = st.text_input("Enter a Keyword to Search (e.g., 'Cricket', 'Politics')")

        if st.button("Find Articles"):
            if keyword:
                with st.spinner("Detecting keyword language..."):
                    try:
                        detected_language = GoogleTranslator(source='auto', target='en').translate(keyword)
                    except Exception as e:
                        st.error(f"Error during language detection: {e}")
                        detected_language = keyword
                    if detected_language == keyword:
                        st.info(f"Keyword detected in English: '{keyword}'")
                        translated_keyword = keyword
                    else:
                        st.info(f"Keyword detected in Gujarati: '{keyword}'")
                        translated_keyword = keyword

                with st.spinner("Searching for articles..."):
                    links = fetch_article_links_by_keyword(base_url, translated_keyword)

                    if links:
                        st.success(f"Found {len(links)} articles for the keyword '{translated_keyword}':")
                        for i, link in enumerate(links, start=1):
                            with st.spinner(f"Extracting content from article {i}..."):
                                article_date, article_content = extract_article(link, newspaper)
                                st.write(f"**Published on:** {article_date}")

                                if article_content:
                                    st.write(f"**Article Content (Without Links):**\n{article_content}")
                                else:
                                    st.warning(f"Article {i} has no content.")
                    else:
                        st.warning(f"No articles found for the keyword '{translated_keyword}'. Try using a different keyword.")
            else:
                st.error("Please enter a keyword to search for articles.")

    elif search_method == "By Date":
        date_input = st.date_input("Pick a date to search articles")
        date_str = date_input.strftime('%Y-%m-%d')  # Format the date as YYYY-MM-DD

        if st.button("Find Articles by Date"):
            with st.spinner(f"Searching for articles from {date_str}..."):
                links = fetch_article_links_by_date(base_url, date_str)

                if links:
                    st.success(f"Found {len(links)} articles for the date '{date_str}':")
                    for i, link in enumerate(links, start=1):
                        with st.spinner(f"Extracting content from article {i}..."):
                            article_date, article_content = extract_article(link, newspaper)
                            st.write(f"**Published on:** {article_date}")

                            if article_content:
                                st.write(f"**Article Content (Without Links):**\n{article_content}")
                            else:
                                st.warning(f"Article {i} has no content.")
                else:
                    st.warning(f"No articles found for the date '{date_str}'. Try using a different date.")

if __name__ == "__main__":
    main()
