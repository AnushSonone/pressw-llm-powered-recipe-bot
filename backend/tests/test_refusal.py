"""Tests for the refusal node (out-of-scope response)."""

from graphs.refusal import REFUSAL_MESSAGE, refusal_node


def test_refusal_node_returns_refusal_message():
    state = {"message": "What is the capital of France?"}
    out = refusal_node(state)
    assert out["refusal"] == REFUSAL_MESSAGE
    assert out["answer"] is None


def test_refusal_node_accepts_minimal_state():
    state = {"message": "anything"}
    out = refusal_node(state)
    assert out["refusal"] == REFUSAL_MESSAGE
    assert out["answer"] is None
