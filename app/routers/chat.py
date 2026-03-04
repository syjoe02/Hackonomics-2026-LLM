# app/routers/chat.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/stream")
def chat_stream(
    req: ChatRequest,
    db: Session = Depends(get_db),
):
    service = ChatService()

    def event_stream():
        try:
            yield ": connected\n\n"

            for token in service.stream_chat(
                db=db,
                user_id="demo-user",  # TODO: replace with JWT
                question=req.question,
                news=req.news,
            ):
                yield f"data: {token}\n\n"

        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )