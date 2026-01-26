from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from summarise import generate_summary
from scrape import get_news_articles
# import time
import requests
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### ADded the cors again
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
    raw_news = get_news_articles()  

    result = {"national": [], "international": []}

    for section in ["national", "international"]:
        if raw_news.get(section):
            articles = raw_news[section][:10]  
            for item in articles:
                text = item.get("text", title)  
                url = item.get("url", "")
                # image = item.get("image", None)
                url_new = item.get("url","")

                summary = safe_generate_summary(text)
                result[section].append({
                    "title": title,
                    "summary": summary,
                    "url": url
                })
                time.sleep(1)  

    return result
@app.get("/details")
def ping():
    return {"message": "found"}
