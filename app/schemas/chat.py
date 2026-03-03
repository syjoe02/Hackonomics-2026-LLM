from pydantic import BaseModel
from typing import List

class NewsItem(BaseModel):
    title: str
    description: str

class ChatRequest(BaseModel):
    question: str
    news: List[NewsItem]

class ChatResponse(BaseModel):
    answer: str