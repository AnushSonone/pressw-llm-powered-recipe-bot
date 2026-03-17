"""
State type for the cooking Q&A LangGraph. All nodes read and return updates to this state.
"""

from typing import TypedDict


class CookingState(TypedDict, total=False):
    """State passed through the graph. Keys are optional for partial updates."""

    message: str
    is_cooking_query: bool
    refusal: str | None
    answer: str | None
    reasoning_chain: list
    debug: bool
