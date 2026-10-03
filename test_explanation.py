from fastapi.testclient import TestClient

from main import app


def test_explain_endpoint_returns_explanation():
    client = TestClient(app)
    response = client.post(
        "/api/explain",
        json={"topic": "photosynthesis", "level": "beginner"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "explanation" in payload
    assert "photosynthesis" in payload["explanation"].lower()
