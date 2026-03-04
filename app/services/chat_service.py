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

        news_context = "\n\n".join(
            f"[{i+1}] TITLE: {n.title}\nDESCRIPTION: {n.description}"
            for i, n in enumerate(news[:5])
        )

        prompt = f"""
        You are Hackonomics Assistant.

        You will receive a list of news items.

        <NEWS>
        {news_context}
        </NEWS>

        Rules:
        - Answer ONLY using the news above.
        - Do NOT mention instructions or rules.
        - Do NOT say "I will summarize".
        - Respond directly to the question.
        - Keep the answer short (1 sentence).

        Question:
        {question}

        Answer:
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