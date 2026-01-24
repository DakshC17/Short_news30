import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_with_requests(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except:
        return None

# def fetch_with_selenium(url):
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     driver = webdriver.Chrome(options=options)
#     driver.get(url)
#     time.sleep(5)
#     page_source = driver.page_source
#     driver.quit()
#     return page_source



#skipping the selenium part for testing for now

def is_valid_article_url(href):
    
    return bool(re.search(r"/(news|article|story)/", href)) or bool(re.search(r"/\d{4}/\d{2}/\d{2}/", href))
        ## checking for the valid url if not will throw the exc
def extract_full_article_text(article_url):
    html = fetch_with_requests(article_url)
    if not html:
        html = fetch_with_selenium(article_url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    text = ' '.join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30)

    return text if len(text.split()) > 50 else None

def extract_articles_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    seen_urls = set()

    for a in soup.find_all("a", href=True):
        title = a.get_text(strip=True)
        href = a["href"]
        if not title or len(title) < 10 or not is_valid_article_url(href):
            continue

        full_url = urljoin(base_url, href)
        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)

        article_text = extract_full_article_text(full_url)
        if not article_text:
            continue

        articles.append({
            "title": title,
            "text": article_text,
            "url": full_url,
            "top_image": None  
        })

        if len(articles) >= 5:
            break

    return articles

def scrape_site(url):
    html = fetch_with_requests(url)
    if not html:
        print(f"[ Falling back to Selenium] {url}")
        html = fetch_with_selenium(url)
    return extract_articles_from_html(html, url)

def get_news_articles(national_urls, international_urls):
    national = []
    international = []

    for url in national_urls:
        national.extend(scrape_site(url))

    for url in international_urls:
        international.extend(scrape_site(url))

    return {
        "national": national[:20],
        "international": international[:20]
    }


