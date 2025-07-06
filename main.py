from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from summarise import generate_summary
from scrape import get_news_articles
import time
import requests

app = FastAPI()

# Allow CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Retry wrapper to handle rate limits (429) with exponential backoff
def safe_generate_summary(text, retries=3):
    for attempt in range(retries):
        try:
            return generate_summary(text)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 2 * (attempt + 1)
                print(f"[Rate Limit] Retry {attempt + 1}/{retries} after {wait_time}s")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            print(f"[Error in Summary] {e}")
            break
    return "Summary unavailable due to rate limiting or an error."

@app.get("/news")
def get_summarised_news():
    raw_news = get_news_articles()  # From pygooglenews version

    result = {"national": [], "international": []}

    for section in ["national", "international"]:
        if raw_news.get(section):
            item = raw_news[section][0]  # Take only the first news article
            title = item.get("title", "")
            text = item.get("text", title)  # Fallback to title if text is missing
            url = item.get("url", "")
            image = item.get("image", None)

            summary = safe_generate_summary(text)
            result[section].append({
                "title": title,
                "summary": summary,
                "url": url
            })
            time.sleep(1)  # Optional: prevent immediate burst

    return result
  # Optional: control request burst rate

    return result
    