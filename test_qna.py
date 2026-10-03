from fastapi.testclient import TestClient

from gemini_client import _fallback_text
from main import app


def test_qna_endpoint_returns_answer():
    client = TestClient(app)
    response = client.post("/api/qna", json={"question": "What is photosynthesis?"})

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert data["answer"].strip()


def test_fallback_question_answer_is_specific_and_helpful():
    answer = _fallback_text("Question: What is a cell?")

    assert "cell" in answer.lower()
    assert any(word in answer.lower() for word in ["basic", "unit", "living", "tiny", "structure"])
