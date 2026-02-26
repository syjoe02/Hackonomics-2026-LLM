from pydantic import BaseModel
from typing import List

class NewsItem(BaseModel):
    title: str
    description: str

class ChatRequest(BaseModel):
    question: str
    country_code: str
    news: List[NewsItem]