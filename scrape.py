from pygooglenews import GoogleNews

gn = GoogleNews(lang='en', country='IN')

def fetch_articles(section: str, limit=10):
    """
    Fetches top news articles from a specified Google News topic.
    Sections: 'nation', 'world', 'business', 'technology', etc.
    """
    try:
        feed = gn.topic_headlines(section.upper())
    except Exception as e:
        print(f"[❌ Error fetching {section.upper()} news] {e}")
        return []

    articles = []

    for entry in feed['entries'][:limit]:
        articles.append({
            "title": entry.get("title", "No Title"),
            "text": entry.get("summary", entry.get("title", "")),  
            "url": entry.get("link", ""),
            
        })


    
    return articles

def get_news_articles():
    return {
        "national": fetch_articles("nation", limit=10),
        "international": fetch_articles("world", limit=10)
    }

