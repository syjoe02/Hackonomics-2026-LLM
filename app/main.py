from fastapi import FastAPI
from app.routers import chat

app = FastAPI(title="LLM Service")

app.include_router(chat.router, prefix="/api")