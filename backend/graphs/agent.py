"""
Agent node: answer cooking queries using the LLM and tools (search, cookware check).
The LLM decides when to call tools; we run them and loop until we get a final answer.
"""

import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from graphs.state import CookingState
from llm import get_chat_model
from tools.cookware import check_cookware
from tools.search import search_tool

logger = logging.getLogger(__name__)

AGENT_SYSTEM = """You are a helpful cooking and recipe assistant. Answer the user's question about cooking, recipes, or ingredients.

You have two tools:
1. search: use this to look up recipes, cooking techniques, or ingredient info when you don't know or want to double-check.
2. check_cookware: use this when you suggest a recipe. Input is a comma-separated list of required equipment (e.g. "Frying Pan, Knife, Stovetop"). Tell the user if they can make it with their equipment or what they're missing.

Give clear steps, tips, and mention equipment when relevant. If you use check_cookware, include that result in your answer."""

TOOLS = [search_tool, check_cookware]


def agent_node(state: CookingState) -> dict:
    """
    Run the LLM with tools until we get a final answer. Updates state with answer and optional reasoning_chain.
    """
    message = state["message"]
    debug = state.get("debug", False)
    reasoning_chain = list(state.get("reasoning_chain") or [])

    logger.info("agent_node: processing cooking query")
    reasoning_chain.append({"node": "agent", "input_preview": message[:80]})

    llm = get_chat_model(temperature=0.2).bind_tools(TOOLS)
    messages = [
        SystemMessage(content=AGENT_SYSTEM),
        HumanMessage(content=message),
    ]

    while True:
        response = llm.invoke(messages)
        if not isinstance(response, AIMessage):
            break
        if not (response.tool_calls and len(response.tool_calls) > 0):
            break
        messages.append(response)
        tools_by_name = {t.name: t for t in TOOLS}
        for tc in response.tool_calls:
            name = tc.get("name", "")
            args = tc.get("args", {}) if isinstance(tc.get("args"), dict) else {}
            tid = tc.get("id", "")
            logger.info("agent_node: tool_call name=%s", name)
            if debug:
                reasoning_chain.append({"tool_call": name, "args": args})
            tool = tools_by_name.get(name)
            if tool:
                try:
                    result = tool.invoke(args)
                except Exception as e:
                    result = f"Tool error: {e}"
            else:
                result = "Unknown tool"
            if debug:
                reasoning_chain.append({"tool_result_preview": str(result)[:200]})
            messages.append(ToolMessage(content=str(result), tool_call_id=tid))
    answer = response.content if hasattr(response, "content") else str(response)
    reasoning_chain.append({"node": "agent", "result_preview": (answer or "")[:100]})

    return {
        "answer": answer,
        "refusal": None,
        "reasoning_chain": reasoning_chain if debug else None,
    }
