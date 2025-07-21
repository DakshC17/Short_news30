import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY is missing. Make sure it's defined in your .env file.")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def generate_summary(text: str, model="qwen/qwen3-14b:free") -> str:
    prompt = (
        "Summarize the following news article in no more than 30 words. "
        "IMPORTANT: Only return the summary. Do NOT include any reasoning, thinking steps, or markdown. Just the plain summary text.\n\n"
        f"{text}"
    )

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)
    response.raise_for_status()

    summary = response.json()["choices"][0]["message"]["content"]

    # Optional: clean up if model adds extra text
    return summary.strip()
