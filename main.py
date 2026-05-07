import re
import textwrap
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Casio FX-82MS API Bridge")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

SYSTEM_PROMPT = """
You are a helpful and intelligent AI assistant. 

Formatting Rules:
- No markdown, bullets, or emojis.
- Keep sentences relatively short for easy reading.
- Do not use long paragraphs; use newlines for separate ideas.
"""

class ChatRequest(BaseModel):
    prompt: str

def oled_format(text: str, width: int = 18, max_lines: int = 4) -> str:
    text = text.strip()
    # Remove markdown-ish characters
    text = re.sub(r"[*_`#>\-•]", "", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Wrap for OLED
    lines = textwrap.wrap(text, width=width)
    lines = lines[:max_lines]
    return "\n".join(lines)

def query_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.9,
            "num_predict": 256,
            "repeat_penalty": 1.1,
            "seed": 42
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=45)
    response.raise_for_status()

    raw = response.json().get("response", "")
    # Basic cleanup without truncation
    clean = re.sub(r"[*_`#>\-•]", "", raw)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

@app.post("/ask")
def ask(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        answer = query_ollama(request.prompt)
        return {
            "answer": answer
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama unavailable: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
