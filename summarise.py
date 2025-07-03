import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing. Make sure it's defined in your .env file.")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def generate_summary(text: str, model="llama3-70b-8192") -> str:
    prompt = f"Summarize the following news article in no more than 30 words:**\n\n{text}**"

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles in 30 words."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)
    response.raise_for_status()  # This line will raise 401 if the API key is invalid

    summary = response.json()["choices"][0]["message"]["content"]
    return summary.strip()
