from sqlalchemy.orm import Session
from app.models.chat import ChatSession, ChatMessage


class ChatRepository:

    def create_session(self, db: Session, user_id: str) -> ChatSession:
        session = ChatSession(user_id=user_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def get_session(self, db: Session, session_id):
        return db.get(ChatSession, session_id)

    def save_message(
        self,
        db: Session,
        session_id,
        role: str,
        content: str,
    ):
        msg = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg