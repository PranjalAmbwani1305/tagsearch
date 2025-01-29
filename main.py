import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime

# Function to scrape articles
def fetch_articles(keyword, date):
    base_url = "https://www.gujaratsamachar.com/"
    date_str = date.strftime("%Y-%m-%d")  # Format date as per the website's requirements
    search_url = f"{base_url}?search={keyword}&date={date_str}"
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    articles = []
    # Assuming the website stores article content in <div class="article">
    for article in soup.find_all("div", class_="article"):
        title = article.find("h2").text.strip()
        content = article.find("p").text.strip()
        articles.append({"title": title, "content": content})
    
    return articles


def app():
    st.title("Gujarati Newspaper Article Search")
    
   
    keyword = st.text_input("Enter keyword", "")
    date = st.date_input("Select Date", datetime.date.today())
    
    if st.button("Search"):
        if keyword:
            articles = fetch_articles(keyword, date)
            
            if articles:
                for article in articles:
                    st.subheader(article["title"])
                    st.write(article["content"])
            else:
                st.write("No articles found.")
        else:
            st.write("Please enter a keyword.")

if __name__ == "__main__":
    app()
