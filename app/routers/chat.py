from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.services.ollama_service import ask_llm

router = APIRouter()

@router.post("/chat")
def chat(req: ChatRequest):
    answer = ask_llm(req.question, req.news, req.country_code)
    return {"answer": answer}