from typing import Generator
from sqlalchemy.orm import Session

from adapter.chat_repository import ChatRepository
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

        if session_id:
            session = self.repo.get_session(db, session_id)
        else:
            session = self.repo.create_session(db, user_id)

        self.repo.save_message(db, session.id, "user", question)

        news_context = "\n".join(
            f"- {n.title}: {n.description}" for n in news
        )

        prompt = f"""
        You are Hackonomics Assistant.

        Business News Context:
        {news_context}

        User:
        {question}

        Assistant:
        """

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