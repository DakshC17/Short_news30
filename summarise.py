import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def generate_summary(text: str, model="llama3-70b-8192") -> str:
    prompt = f"Summarize the following news article in no more than 30 words:\n\n{text}"

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)
    response.raise_for_status()

    summary = response.json()["choices"][0]["message"]["content"]
    return summary.strip()
