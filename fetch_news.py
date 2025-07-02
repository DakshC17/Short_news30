from newspaper import Article
from typing import List, Dict

def extract_article(url: str) -> Dict:
    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            "title": article.title,
            "text": article.text,
            "top_image": article.top_image,
            "url": url
        }
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def get_news_articles(national_urls: List[str], international_urls: List[str]) -> Dict[str, List[Dict]]:
    national = []
    international = []

    for url in national_urls:
        article = extract_article(url)
        if article: national.append(article)

    for url in international_urls:
        article = extract_article(url)
        if article: international.append(article)

    return {
        "national": national[:10],
        "international": international[:10]
    }
