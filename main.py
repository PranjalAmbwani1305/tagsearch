def extract_article(link, newspaper, target_date, processed_links):
    try:
        if link in processed_links:  # Skip already processed links
            return "", ""

        processed_links.add(link)  # Mark this link as processed

        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        article_date = "Date not found"
        article_text = ""

        # Extract date
        if newspaper == "Gujarat Samachar":
            date_element = soup.find('span', class_='post-date')
            if date_element:
                article_date = date_element.get_text(strip=True)

        # Try parsing the article date to a datetime object, handle cases with time included
        try:
            # If the date includes time, split it and use only the date part
            article_date_obj = datetime.strptime(article_date.split(' ')[0], '%Y-%m-%d')
        except Exception as e:
            article_date_obj = None

        # Check if the article's date matches the target date
        if article_date_obj and article_date_obj.date() != target_date.date():
            return article_date, ""

        # Extract content
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
