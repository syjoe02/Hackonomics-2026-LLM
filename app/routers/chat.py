from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.chat_service import stream_news_answer

router = APIRouter()


@router.post("/stream")
def chat_stream(req: ChatRequest):

    def event_stream():
        try:
            yield ": connected\n\n"

            for token in stream_news_answer(req.question, req.news):
                yield f"data: {token}\n\n"

        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )