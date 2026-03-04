import logging
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Generator

from app.core.database import get_db
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/stream")
def chat_stream(
    req: ChatRequest,
    db: Session = Depends(get_db),
):

    logger.info("Chat request received")
    logger.info("Question: %s", req.question)
    logger.info("News count: %s", len(req.news))

    service = ChatService()

    def event_stream() -> Generator[str, None, None]:

        try:
            yield ": connected\n\n"

            for token in service.stream_chat(
                db=db,
                user_id="demo-user",
                question=req.question,
                news=req.news,
            ):
                yield f"data: {token}\n\n"

        except Exception as e:
            logger.exception("LLM stream error")

            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )