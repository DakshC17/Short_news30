from pygooglenews import GoogleNews


#py news is failing need to try on different approach

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


    ##this array will hold on the scraped newss..

    # for entry in feed['entries'][:limit]:
    #     articles.append({
    #         "title": entry.get("title", "No Title"),
    #         "text": entry.get("summary", entry.get("title", "")),  
    #         "url": entry.get("link", ""),
            
    #     })


    for entry in feed['entries'][:limit]:
        articles.append({})

    #keeping it empty as of now need to change the approach


    
    return articles

def get_news_articles():
    return {
        "national": fetch_articles("nation", limit=10),
        "international": fetch_articles("world", limit=10)
    }

##national and world later will expand to other news


