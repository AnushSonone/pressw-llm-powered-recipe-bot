"""
External info tool: web search via DuckDuckGo (no API key).
The LLM can invoke this to research recipes or cooking questions.
"""

import logging

from langchain_community.tools import DuckDuckGoSearchRun

logger = logging.getLogger(__name__)

search_tool = DuckDuckGoSearchRun()


def run_search(query: str) -> str:
    """Run a web search. Used by the agent to look up recipes or cooking info."""
    logger.info("search_tool: query=%s", query[:80])
    result = search_tool.invoke({"query": query})
    return result if isinstance(result, str) else str(result)
