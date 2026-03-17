"""Tests for the agent node. Mocks LLM to avoid network and tool calls."""

from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage

from graphs.agent import agent_node


@patch("graphs.agent.get_chat_model")
def test_agent_node_returns_answer_without_tool_calls(mock_get_chat_model):
    # LLM returns a final answer (no tool_calls)
    mock_llm = MagicMock()
    mock_llm.bind_tools.return_value = mock_llm
    mock_llm.invoke.return_value = AIMessage(
        content="Here is how you make pasta: boil water, add pasta, drain.",
        tool_calls=[],
    )
    mock_get_chat_model.return_value = mock_llm

    state = {"message": "How do I make pasta?"}
    out = agent_node(state)

    assert out["answer"] is not None
    assert "pasta" in out["answer"].lower() or len(out["answer"]) > 0
    assert out["refusal"] is None
