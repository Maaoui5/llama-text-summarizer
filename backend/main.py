from fastapi import FastAPI, Form, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama local API

@app.post("/summarize/")
def summarize(text: str = Form(...)):
    prompt = f"Summarize the following text in 3-5 concise sentences:\n\n{text}"
    payload = {
        "model": "llama3:8b",    # change if your local model name differs
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Ollama: {e}")

    data = resp.json()
    # Ollama's non-streaming response commonly contains a "response" field (fallbacks below)
    summary = data.get("response") or data.get("output") or data.get("choices", [{}])[0].get("text")
    if not summary:
        raise HTTPException(status_code=500, detail=f"Unexpected Ollama response: {data}")
    return {"summary": summary.strip()}
