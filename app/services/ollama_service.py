import requests
from app.core.config import OLLAMA_URL

def ask_llm(question: str, news: list, country_code: str):
    prompt = f"""
    You are a financial analyst.

    Country: {country_code}

    Business news:
    {news}

    Question:
    {question}

    Answer clearly and concisely.
    """

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )

    return response.json()["response"]