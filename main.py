from fastapi import FastAPI
from scraper.fetch_news import get_news_articles
from summariser.summarise import generate_summary
import uvicorn

# Define your custom news URLs
national_urls = [
    "https://timesofindia.indiatimes.com/india/modi-speech-today-live-updates/...",
    "https://www.hindustantimes.com/india-news/...",
    "https://www.thehindu.com/news/national/..."
]

international_urls = [
    "https://www.bbc.com/news/world",
    "https://edition.cnn.com/world",
    "https://www.reuters.com/world/"
]

app = FastAPI()

@app.get("/news")
def get_summarised_news():
    raw_news = get_news_articles(national_urls, international_urls)
    result = {"national": [], "international": []}

    for item in raw_news["national"]:
        summary = generate_summary(item["text"])
        result["national"].append({
            "title": item["title"],
            "summary": summary,
            "image": item["top_image"],
            "url": item["url"]
        })

    for item in raw_news["international"]:
        summary = generate_summary(item["text"])
        result["international"].append({
            "title": item["title"],
            "summary": summary,
            "image": item["top_image"],
            "url": item["url"]
        })

    return result

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
