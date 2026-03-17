"""
Compiled LangGraph: classify -> (refusal | agent). All LLM calls go through LangChain.
"""

import logging

from langgraph.graph import END, StateGraph

from graphs.agent import agent_node
from graphs.classify import classify_node
from graphs.refusal import refusal_node
from graphs.state import CookingState

logger = logging.getLogger(__name__)


def _route_after_classify(state: CookingState) -> str:
    """Conditional edge: go to refusal or agent."""
    if state.get("is_cooking_query"):
        logger.info("graph: routing to agent")
        return "agent"
    logger.info("graph: routing to refusal")
    return "refusal"


def build_cooking_graph():
    """Build and compile the cooking Q&A graph."""
    builder = StateGraph(CookingState)

    builder.add_node("classify", classify_node)
    builder.add_node("refusal", refusal_node)
    builder.add_node("agent", agent_node)

    builder.set_entry_point("classify")
    builder.add_conditional_edges(
        "classify", _route_after_classify, {"refusal": "refusal", "agent": "agent"}
    )
    builder.add_edge("refusal", END)
    builder.add_edge("agent", END)

    return builder.compile()


# Singleton compiled graph for the app
_cooking_graph = None


def get_cooking_graph():
    global _cooking_graph
    if _cooking_graph is None:
        _cooking_graph = build_cooking_graph()
    return _cooking_graph
