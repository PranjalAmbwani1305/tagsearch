import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime

def extract_article(link, newspaper, date_str):
    article_date = "Date not found"
    article_text = ""

    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        date_tag = soup.find('time')
        if date_tag:
            article_date = date_tag.get_text(strip=True)

        if date_str and article_date != date_str:
            return article_date, None

        content = soup.find('div', {'class': 'article-content'})
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
    return article_date, None

def main():
    st.title("Article Finder")
    newspaper = st.sidebar.selectbox("Select a Newspaper", ("Gujarat Samachar",))
    date_str = st.sidebar.date_input("Select Date", datetime.today().date()).strftime('%Y-%m-%d')
    keyword = st.sidebar.text_input("Enter Keyword to Search")

    if keyword:
        search_url = f"https://www.gujaratsamachar.com/search/{keyword.replace(' ', '+')}"
        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = set()
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                if 'gujaratsamachar.com' in link and link not in links:
                    links.add(link)
            
            unique_links = set()
            for link in links:
                if link not in unique_links:
                    unique_links.add(link)
                    st.write(f"**Article Link:** {link}")
                    with st.spinner(f"Extracting content..."):
                        article_date, article_content = extract_article(link, newspaper, date_str)
                        if article_content:
                            st.write(f"**Published on:** {article_date}")
                            st.write(f"**Article Content (Without Links):**\n{article_content}")
                        else:
                            st.warning(f"Article does not match the date '{date_str}' or has no content.")
        else:
            st.warning("No articles found for this keyword.")
    else:
        st.warning("Please enter a keyword to search.")
        
if __name__ == "__main__":
    main()
