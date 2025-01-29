import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

def fetch_article_links(base_url, keyword, date_str):
    try:
        search_url = f"{base_url}?date={date_str}&q={keyword}"
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        links = []
        for a in soup.find_all('a', href=True):
            if keyword.lower() in a.get('href', '').lower() or keyword.lower() in a.text.lower():
                href = a['href']
                if not href.startswith("http"):
                    href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"

                # Debug output to track found links
                st.write(f"Found link: {href} (matching keyword: {keyword})")

                links.append(href)
        return links
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        st.error(f"Oops! Something went wrong while fetching the links: {e}")
        return []

def extract_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract article date
        article_date = "Date not found"
        date_element = soup.find('span', class_='post-date')
        if date_element:
            article_date = date_element.get_text(strip=True)

        # Debug output for date
        st.write(f"Article Date: {article_date} (Link: {link})")

        article_text = ""
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
            st.warning("Article content not found.")

        return article_date, article_text.strip() if article_text else "No article content found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching article content: {e}", ""
    except Exception as e:
        return f"Error extracting article: {e}", ""

def main():
    st.set_page_config(page_title="Gujarati News Article Scraper", page_icon="📰")
    st.title("Gujarati News Article Finder")

    st.markdown("""
    **Welcome to the Gujarat Samachar Article Finder!**
    This tool allows you to search for articles from Gujarat Samachar.
    Enter a keyword and select a date, and we'll find relevant articles for you!
    """)

    base_url = "https://www.gujaratsamachar.com/"

    keyword = st.text_input("Enter a Keyword to Search (e.g., 'Cricket', 'Politics')")

    # Date Picker to select a date
    selected_date = st.date_input("Select a Date", min_value=datetime(2020, 1, 1))

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

            # Format the selected date as YYYY-MM-DD
            date_str = selected_date.strftime("%Y-%m-%d")
            st.write(f"Searching articles for the keyword '{translated_keyword}' on {date_str}...")

            with st.spinner("Searching for articles..."):
                links = fetch_article_links(base_url, translated_keyword, date_str)

                if links:
                    st.success(f"Found {len(links)} articles for the keyword '{translated_keyword}':")
                    for i, link in enumerate(links, start=1):
                        st.write(f"**Article {i} (Link):** {link}")
                        with st.spinner(f"Extracting content from article {i}..."):
                            article_date, article_content = extract_article(link)
                            st.write(f"**Published on:** {article_date}")

                            if article_content:
                                st.write(f"**Article Content (Without Links):**\n{article_content}")
                            else:
                                st.warning(f"Article {i} has no content.")
                else:
                    st.warning(f"No articles found for the keyword '{translated_keyword}' on {date_str}. Try using a different keyword.")
        else:
            st.error("Please enter a keyword to search for articles.")

if __name__ == "__main__":
    main()
