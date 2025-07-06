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

def generate_summary(text: str, model="qwen/qwen3-32b") -> str:
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
    
    # Post-clean the summary to remove any <think> tags if still present
    if "<think>" in summary:
        summary = summary.split("</think>")[-1].strip()

    return summary.strip()
