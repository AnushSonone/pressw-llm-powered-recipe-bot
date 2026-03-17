"""
FastAPI entry point for the LLM-powered cooking & recipe Q&A API.
"""

import json
import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = (os.getenv("LOG_LEVEL") or "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from graphs.graph import get_cooking_graph
from schemas.cooking import CookingRequest, CookingResponse

app = FastAPI(
    title="PressW Recipe Q&A API",
    description="LLM-powered cooking and recipe Q&A backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every request and response status for a full audit trail."""
    method = request.method
    path = request.url.path
    client = getattr(request.client, "host", "?") if request.client else "?"
    logger.info("request_start method=%s path=%s client=%s", method, path, client)
    response = await call_next(request)
    logger.info("request_end method=%s path=%s status=%s", method, path, response.status_code)
    return response


@app.on_event("startup")
def startup_log():
    """Log API key and config status only. Never log key values."""
    groq = "set" if os.getenv("GROQ_API_KEY") else "not set"
    logger.info("config GROQ_API_KEY=%s LOG_LEVEL=%s", groq, LOG_LEVEL)


@app.get("/health")
def health():
    """Health check for Docker and load balancers."""
    return {"status": "ok"}


@app.post("/api/cooking", response_model=CookingResponse)
def cooking_post(body: CookingRequest):
    """
    Handle a cooking/recipe query. Returns either a refusal (out-of-scope) or a full answer.
    Set debug=true in the body to include reasoning_chain in the response.
    """
    logger.info("POST /api/cooking message_len=%s debug=%s", len(body.message), body.debug)
    graph = get_cooking_graph()
    initial = {"message": body.message, "debug": body.debug}
    final = graph.invoke(initial)
    refusal = final.get("refusal")
    answer = final.get("answer")
    reasoning_chain = final.get("reasoning_chain") if body.debug else None
    return CookingResponse(refusal=refusal, answer=answer, reasoning_chain=reasoning_chain)


@app.post("/api/cooking/stream")
def cooking_stream(body: CookingRequest):
    """
    Same as POST /api/cooking but streams the response as SSE so the frontend can show progress.
    """

    def event_stream():
        try:
            logger.info("POST /api/cooking/stream message_len=%s", len(body.message))
            graph = get_cooking_graph()
            final = graph.invoke({"message": body.message, "debug": body.debug})
            payload = {
                "refusal": final.get("refusal"),
                "answer": final.get("answer"),
                "reasoning_chain": final.get("reasoning_chain") if body.debug else None,
            }
            yield f"data: {json.dumps(payload)}\n\n"
        except Exception as e:
            logger.exception("cooking_stream error")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
