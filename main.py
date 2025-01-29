import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
from deep_translator import GoogleTranslator


def fetch_articles(keyword, date):
    base_url = "https://www.gujaratsamachar.com/"
    date_str = date.strftime("%Y-%m-%d")  
    search_url = f"{base_url}?date={date_str}"
    
    st.write(f"Search URL: {search_url}")  
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    articles = []
    for article in soup.find_all("div", class_="article"):
        title = article.find("h2").text.strip()
        content = article.find("p").text.strip()
        articles.append({"title": title, "content": content})
    
    return articles



def translate_text(text, target_lang="en"):
    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated_text
    except Exception as e:
        st.error(f"Error during translation: {e}")
        return text


def app():
    st.title("Gujarati Newspaper Article Search")
    
    keyword = st.text_input("Enter keyword", "")
    date = st.date_input("Select Date", datetime.date.today())
    target_lang = st.selectbox("Select Target Language for Translation", ["English", "Gujarati"])
    
    lang_map = {"English": "en", "Gujarati": "gu"}
    
    if st.button("Search"):
        if keyword:
            articles = fetch_articles(keyword, date)
            
            if articles:
                for article in articles:
                    st.subheader(article["title"])
                    if target_lang == "English":
                        translated_content = translate_text(article["content"], target_lang=lang_map[target_lang])
                        st.write(translated_content)
                    else:
                        st.write(article["content"])
            else:
                st.write("No articles found.")
        else:
            st.write("Please enter a keyword.")


if __name__ == "__main__":
    app()
