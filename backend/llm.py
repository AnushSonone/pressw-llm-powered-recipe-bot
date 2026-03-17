"""
LLM access via LangChain only. All model calls go through this module.
Uses Groq (ChatGroq) so we never touch model-specific SDKs directly.
"""

import os

from langchain_groq import ChatGroq


def get_chat_model(model: str = "llama-3.1-8b-instant", temperature: float = 0.2):
    """
    Return a LangChain chat model (Groq). Used by LangGraph and tools.
    Set GROQ_API_KEY in .env.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Get a free key at https://console.groq.com")
    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=api_key,
    )
