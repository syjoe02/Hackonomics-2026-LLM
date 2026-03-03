from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_URL: str = "http://ollama:11434/api/generate"
    OLLAMA_MODEL: str = "llama3"

settings = Settings()