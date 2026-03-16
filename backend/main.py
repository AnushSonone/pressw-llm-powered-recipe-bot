"""
FastAPI entry point for the LLM-powered cooking & recipe Q&A API.
"""
from fastapi import FastAPI

app = FastAPI(
    title="PressW Recipe Q&A API",
    description="LLM-powered cooking and recipe Q&A backend",
    version="0.1.0",
)


@app.get("/health")
def health():
    """Health check for Docker and load balancers."""
    return {"status": "ok"}
