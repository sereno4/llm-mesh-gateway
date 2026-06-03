from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import httpx
import re

app = FastAPI()

INTENT_PATTERNS = {
    "code": [
        r"\b(def|class|import|python|function|code|debug|compile)\b"
    ],
    "analysis": [
        r"\b(analyze|analysis|compare|explain|architecture)\b"
    ],
    "creative": [
        r"\b(story|poem|creative|write)\b"
    ]
}

MODELS = {
    "code": "http://ollama-local:11434",
    "analysis": "http://ollama-local:11434",
    "creative": "http://ollama-local:11434",
    "general": "http://ollama-local:11434"
}

def classify(prompt: str):

    for intent, patterns in INTENT_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, prompt, re.IGNORECASE):
                return intent

    return "general"

@app.get("/health")
async def health():

    return {
        "status": "ok"
    }

@app.post("/v1/chat/completions")
async def completions(request: Request):

    payload = await request.json()

    messages = payload.get("messages", [])

    prompt = ""

    if messages:
        prompt = messages[-1].get("content","")

    intent = classify(prompt)

    backend = MODELS[intent]

    print(f"[ROUTER] intent={intent}")

    async with httpx.AsyncClient(timeout=120) as client:

        response = await client.post(
            f"{backend}/v1/chat/completions",
            json=payload
        )

    body = response.json()

    body["intent"] = intent

    return JSONResponse(body)

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )
