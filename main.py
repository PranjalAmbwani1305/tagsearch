import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

def fetch_article_links(base_url, keyword):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            if keyword.lower() in a.get('href', '').lower() or keyword.lower() in a.text.lower():
                href = a['href']
                if not href.startswith("http"):
                    href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
                links.add(href)
        return list(links)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        st.error(f"Unexpected error while fetching links: {e}")
        return []

def extract_article(link, newspaper, target_date, processed_links):
    try:
        if link in processed_links:
            return "", ""

        processed_links.add(link)

        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        article_date = "Date not found"
        article_text = ""

        if newspaper == "Gujarat Samachar":
            date_element = soup.find('span', class_='post-date')
            if date_element:
                article_date = date_element.get_text(strip=True)

        try:
            article_date_obj = datetime.strptime(article_date, '%b %d, %Y')
        except Exception:
            article_date_obj = None

        if article_date_obj and article_date_obj.date() != target_date.date():
            return article_date, ""

        content = soup.find('div', class_='td-post-content')
        if content:
            paragraphs = content.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text:
                    article_text += text + "\n"
        else:
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text:
                    article_text += text + "\n"

        return article_date, article_text.strip() if article_text else "No article content found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching article content: {e}", ""
    except Exception as e:
        return f"Error extracting article: {e}", ""

def main():
    st.set_page_config(page_title="Gujarati News Article Scraper", page_icon="📰")
    st.title("Gujarati News Article Finder")

    st.markdown("""**Welcome to the Gujarati News Article Finder!**
    This tool allows you to search for articles from popular Gujarati newspapers.
    Enter a keyword, and we'll find relevant articles for you!
    """)

    newspaper_urls = {"Gujarat Samachar": "https://www.gujaratsamachar.com/"}
    base_url = newspaper_urls["Gujarat Samachar"]

    keyword = st.text_input("Enter a Keyword to Search (e.g., 'Cricket', 'Politics')")
    date_input = st.date_input("Select a Date", value=datetime(2025, 1, 19))

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
                else:
                    st.info(f"Keyword detected in Gujarati: '{keyword}'")

            with st.spinner("Searching for articles..."):
                links = fetch_article_links(base_url, keyword)

                if links:
                    st.success(f"Found {len(links)} articles for the keyword '{keyword}':")
                    processed_links = set()
                    for i, link in enumerate(links, start=1):
                        st.write(f"**Article {i} (Link):** {link}")
                        with st.spinner(f"Extracting content from article {i}..."):
                            article_date, article_content = extract_article(link, "Gujarat Samachar", date_input, processed_links)
                            if article_content:
                                st.write(f"**Published on:** {article_date}")
                                st.write(f"**Article Content:**\n{article_content}")
                            else:
                                st.warning(f"Article {i} does not match the selected date or has no content.")
                else:
                    st.warning(f"No articles found for the keyword '{keyword}'. Try using a different keyword.")
        else:
            st.error("Please enter a keyword to search for articles.")

if __name__ == "__main__":
    main()
