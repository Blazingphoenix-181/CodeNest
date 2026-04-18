import os
import json
import subprocess
import tempfile
import traceback
import httpx
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import asyncio

app = FastAPI(title="CodeNest - Offline AI Coding Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = os.getenv("CODENEST_MODEL", "phi3")

SYSTEM_PROMPT = """You are CodeNest, an expert offline AI coding assistant. You help with:
- Writing, debugging, and explaining code in any language
- Code reviews and best practices
- Algorithm design and optimization
- Explaining technical concepts clearly

When writing code, always use markdown code blocks with the language specified.
Be concise but thorough. If you run code, explain what it does and what the output means.
You run 100% locally — the user's code and data never leave their machine."""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: Optional[str] = None
    file_context: Optional[str] = None


class ExecuteRequest(BaseModel):
    code: str
    language: str = "python"


def get_model(req_model: Optional[str] = None) -> str:
    return req_model or DEFAULT_MODEL


async def stream_ollama(messages: list[dict], model: str):
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "num_ctx": 4096,
            "temperature": 0.3,
        }
    }
    async with httpx.AsyncClient(timeout=300) as client:
        async with client.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as resp:
            if resp.status_code != 200:
                yield f"data: {json.dumps({'error': f'Ollama error: {resp.status_code}'})}\n\n"
                return
            async for line in resp.aiter_lines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        token = data.get("message", {}).get("content", "")
                        if token:
                            yield f"data: {json.dumps({'token': token})}\n\n"
                        if data.get("done"):
                            yield f"data: {json.dumps({'done': True})}\n\n"
                    except json.JSONDecodeError:
                        pass


@app.get("/", response_class=HTMLResponse)
async def root():\n    with open("templates/index.html", "r", encoding='utf-8') as f:
        return f.read()


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    model = get_model(req.model)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if req.file_context:
        messages.append({
            "role": "user",
            "content": f"Here is the code/file I want to discuss:\n\n```\n{req.file_context}\n```"
        })
        messages.append({
            "role": "assistant",
            "content": "I've read your file. What would you like to know or do with it?"
        })

    for msg in req.messages:
        messages.append({"role": msg.role, "content": msg.content})

    return StreamingResponse(
        stream_ollama(messages, model),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


@app.post("/execute")
async def execute_code(req: ExecuteRequest):
    if req.language.lower() != "python":
        return {"output": f"Execution of {req.language} not supported yet. Only Python is supported.", "error": False}

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(req.code)
            tmp_path = f.name

        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=10,
        )
        os.unlink(tmp_path)

        output = result.stdout
        if result.stderr:
            output += ("\n" if output else "") + result.stderr

        return {
            "output": output or "(no output)",
            "error": result.returncode != 0,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"output": "Execution timed out (10s limit)", "error": True}
    except Exception as e:
        return {"output": f"Execution error: {str(e)}", "error": True}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.size and file.size > 500_000:
        raise HTTPException(400, "File too large (max 500KB)")
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File must be a text file")
    return {"filename": file.filename, "content": text, "lines": len(text.splitlines())}


@app.get("/models")
async def list_models():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            data = resp.json()
            models = [m["name"] for m in data.get("models", [])]
            return {"models": models, "default": DEFAULT_MODEL}
    except Exception:
        return {"models": [DEFAULT_MODEL], "default": DEFAULT_MODEL, "warning": "Could not reach Ollama"}


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            return {"status": "ok", "ollama": "connected", "model": DEFAULT_MODEL}
    except Exception:
        return {"status": "degraded", "ollama": "disconnected", "model": DEFAULT_MODEL}
