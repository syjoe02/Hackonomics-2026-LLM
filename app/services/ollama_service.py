import json
import requests
from typing import Generator

from app.core.settings import settings

OLLAMA_URL = settings.OLLAMA_URL
MODEL_NAME = settings.OLLAMA_MODEL

_session = requests.Session()

def stream_llama(prompt: str) -> Generator[str, None, None]:
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 80,
            "temperature": 0.2,
            "top_p": 0.9,
            "num_ctx": 1024,
            "num_thread": 4
        },
    }

    try:
        with _session.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=120,
        ) as response:
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                token = data.get("response")
                if token:
                    yield token

                if data.get("done"):
                    break

    except requests.Timeout as exc:
        raise RuntimeError("Ollama request timed out") from exc

    except requests.RequestException as exc:
        raise RuntimeError(f"Ollama connection failed: {exc}") from exc