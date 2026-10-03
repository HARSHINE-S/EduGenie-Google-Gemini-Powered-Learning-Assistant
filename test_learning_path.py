from fastapi.testclient import TestClient

from main import app


def test_learning_path_endpoint_returns_steps():
    client = TestClient(app)
    response = client.post(
        "/api/learning-path",
        json={"subject": "photosynthesis", "student_level": "beginner"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "subject" in payload
    assert "steps" in payload
    assert len(payload["steps"]) >= 1
    assert any("photosynthesis" in str(step).lower() for step in payload["steps"])


def test_recommendations_endpoint_returns_recs():
    client = TestClient(app)
    response = client.post(
        "/api/recommendations",
        json={"subject": "photosynthesis", "student_level": "beginner"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "subject" in payload
    assert "recommendations" in payload
    assert len(payload["recommendations"]) >= 1
    assert any("photosynthesis" in str(item).lower() for item in payload["recommendations"])
