from typing import List, Generator
from app.schemas.chat import NewsItem
from app.services.ollama_service import stream_llama

SYSTEM_PROMPT = """
You are Hackonomics Assistant, an intelligent financial analysis assistant.

Behavior rules:
- Greet users naturally if they greet you.
- Answer general questions briefly and politely.
- If the user asks about finance, markets, economy, or business news,
  provide thoughtful and professional analysis.
- If business news context is provided, use it when relevant.
- If the question is unrelated to finance, answer briefly and steer back
  to financial insights when appropriate.

Tone:
- Clear
- Professional
- Human-like
- Concise but insightful
"""


def build_prompt(question: str, news: List[NewsItem]) -> str:
    news_context = "\n".join(
        f"- {item.title}: {item.description}"
        for item in news
    ) or "No news available."

    context_block = (
        f"\nBusiness News Context:\n{news_context}\n"
        if news_context
        else "\nBusiness News Context: None provided.\n"
    )

    return (
        f"{SYSTEM_PROMPT}\n"
        f"{context_block}\n"
        f"User Message:\n{question}\n\n"
        f"Assistant Response:"
    )



def stream_news_answer(
    question: str,
    news: List[NewsItem],
) -> Generator[str, None, None]:
    prompt = build_prompt(question, news)

    for token in stream_llama(prompt):
        yield token