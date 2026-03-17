"""
Refusal node: produce a brief, polite refusal for out-of-scope queries.
"""

import logging

from graphs.state import CookingState

logger = logging.getLogger(__name__)

REFUSAL_MESSAGE = (
    "I'm only able to help with cooking and recipe questions. "
    "Please ask something about recipes, ingredients, or how to cook a dish."
)


def refusal_node(state: CookingState) -> dict:
    """Set a short refusal message. No LLM call."""
    logger.info("refusal_node: returning out-of-scope refusal")
    return {"refusal": REFUSAL_MESSAGE, "answer": None}
