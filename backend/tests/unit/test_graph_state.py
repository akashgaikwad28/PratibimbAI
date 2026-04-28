from app.graph.state import GraphState
from app.graph.graph import should_retry


def test_default_state_values():
    state = GraphState(topic="test", urls=[])
    assert state.retry_count == 0
    assert state.final_posts == []
    assert state.execution_id is not None
    assert state.errors == []


def test_should_retry_false_when_no_scores():
    state = GraphState(topic="test", urls=[], scores={})
    assert should_retry(state) is False


def test_should_retry_false_when_max_retries_hit():
    state = GraphState(topic="test", urls=[], scores={"clarity": 5.0}, retry_count=2)
    assert should_retry(state) is False


def test_should_retry_true_when_low_score():
    state = GraphState(topic="test", urls=[], scores={"clarity": 4.0}, retry_count=0)
    assert should_retry(state) is True


def test_should_retry_false_when_high_score():
    state = GraphState(topic="test", urls=[], scores={"clarity": 9.0}, retry_count=0)
    assert should_retry(state) is False
