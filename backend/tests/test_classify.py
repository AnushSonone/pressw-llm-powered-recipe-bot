"""Tests for the classify node. Mocks LLM to avoid network."""

from unittest.mock import MagicMock, patch

from graphs.classify import classify_node


def _make_llm_returning(content: str):
    """Return a mock that get_chat_model can return; invoke() returns a message with content."""
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = content
    mock_llm.invoke.return_value = mock_response
    return mock_llm


@patch("graphs.classify.get_chat_model")
def test_classify_node_yes_cooking_query(mock_get_chat_model):
    mock_get_chat_model.return_value = _make_llm_returning("YES")
    state = {"message": "how to make pasta?"}
    out = classify_node(state)
    assert out["is_cooking_query"] is True
    mock_get_chat_model.assert_called_once_with(temperature=0)


@patch("graphs.classify.get_chat_model")
def test_classify_node_no_out_of_scope(mock_get_chat_model):
    mock_get_chat_model.return_value = _make_llm_returning("NO")
    state = {"message": "What is 2 + 2?"}
    out = classify_node(state)
    assert out["is_cooking_query"] is False


@patch("graphs.classify.get_chat_model")
def test_classify_node_debug_includes_reasoning_chain(mock_get_chat_model):
    mock_get_chat_model.return_value = _make_llm_returning("YES")
    state = {"message": "how to make pasta?", "debug": True}
    out = classify_node(state)
    assert out["is_cooking_query"] is True
    assert out["reasoning_chain"] is not None
    assert len(out["reasoning_chain"]) >= 2  # input_preview and result
