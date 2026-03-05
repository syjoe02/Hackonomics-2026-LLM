from typing import Generator
from sqlalchemy.orm import Session

from app.adapter.chat_repository import ChatRepository
from app.services.ollama_service import stream_llama
from app.schemas.chat import NewsItem


class ChatService:

    def __init__(self):
        self.repo = ChatRepository()

    def stream_chat(
        self,
        db: Session,
        user_id: str,
        question: str,
        news: list[NewsItem],
        session_id=None,
    ) -> Generator[str, None, None]:
        
        news = news[:3]

        if session_id:
            session = self.repo.get_session(db, session_id)
        else:
            session = self.repo.create_session(db, user_id)

        self.repo.save_message(db, session.id, "user", question)

        news_context = "\n".join(
            f"[{i+1}] {n.title}"
            for i, n in enumerate(news)
        )

        prompt = f"""
        You will receive a list of news items.

        News:
        {news_context}
        User question: {question}
        Answer in ONE short sentence using the news above.
        """

        print("PROMPT:", prompt, flush=True)

        assistant_full = ""

        for token in stream_llama(prompt):
            assistant_full += token
            yield token

        self.repo.save_message(
            db,
            session.id,
            "assistant",
            assistant_full,
        )