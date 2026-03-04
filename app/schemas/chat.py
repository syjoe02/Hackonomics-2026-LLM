from pydantic import BaseModel, Field
from typing import List


class NewsItem(BaseModel):
    title: str = Field(..., description="News title")
    description: str = Field(..., description="News description")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    news: List[NewsItem] = Field(default_factory=list)