from fastapi.testclient import TestClient

from main import app


def test_quiz_endpoint_returns_questions():
    client = TestClient(app)
    response = client.post(
        "/api/quiz",
        json={"topic": "photosynthesis", "num_questions": 3},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "topic" in payload
    assert "questions" in payload
    assert len(payload["questions"]) >= 1
    assert any("photosynthesis" in str(q).lower() for q in payload["questions"])
