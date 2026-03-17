"""
Classification node: decide if the user query is about cooking/recipes (in-scope) or not.
Uses LLM via LangChain only.
"""

import logging

from langchain_core.messages import HumanMessage, SystemMessage

from graphs.state import CookingState
from llm import get_chat_model

logger = logging.getLogger(__name__)

CLASSIFY_SYSTEM = """You are a classifier. Given a user message, decide if it is about cooking, recipes, or food preparation.
Answer with exactly one word: YES or NO.
- YES: questions about recipes, how to cook, ingredients, meal ideas, cooking techniques, "what can I make with X".
- NO: anything else (sports, math, general chat, off-topic)."""


def classify_node(state: CookingState) -> dict:
    """
    Run the LLM to classify the user message. Returns state updates.
    """
    message = state["message"]
    debug = state.get("debug", False)
    reasoning_chain = list(state.get("reasoning_chain") or [])

    logger.info("classify_node: classifying query")
    reasoning_chain.append({"node": "classify", "input_preview": message[:80]})

    llm = get_chat_model(temperature=0)
    response = llm.invoke(
        [
            SystemMessage(content=CLASSIFY_SYSTEM),
            HumanMessage(content=message),
        ]
    )
    text = (response.content or "").strip().upper()
    is_cooking = "YES" in text

    logger.info("classify_node: is_cooking_query=%s", is_cooking)
    reasoning_chain.append({"node": "classify", "result": {"is_cooking_query": is_cooking}})

    return {
        "is_cooking_query": is_cooking,
        "reasoning_chain": reasoning_chain if debug else None,
    }
