from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers.chat import router as chat_router
from app.core.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 LLM Service starting...")
    Base.metadata.create_all(bind=engine)
    yield  # app runs here
    print("🛑 LLM Service shutting down...")

def create_app() -> FastAPI:
    app = FastAPI(
        title="LLM Service",
        version="1.0.0",
        description="Local LLM service for Hackonomics",
        lifespan=lifespan,
    )

    # Allow django, frontend access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_router, prefix="/chat", tags=["Chat"])

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()