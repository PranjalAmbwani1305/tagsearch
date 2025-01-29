def extract_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        article_date = "Date not found"
        date_element = soup.find('span', class_='post-date')
        if not date_element:
            date_element = soup.find('time', class_='entry-date')
        if not date_element:
            date_element = soup.find('div', class_='date')
        if date_element:
            article_date = date_element.get_text(strip=True)

        st.write(f"Article Date: {article_date} (Link: {link})")

        article_text = ""
        content = soup.find('div', class_='td-post-content')
        if not content:
            content = soup.find('div', class_='article-body')
        if not content:
            content = soup.find('div', class_='content-body')

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
