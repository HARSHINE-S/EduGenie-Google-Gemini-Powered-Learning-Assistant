from fastapi.testclient import TestClient

from main import app


def test_summarize_endpoint_returns_summary():
    client = TestClient(app)
    response = client.post(
        "/api/summarize",
        json={
            "text": "Photosynthesis is the process plants use to convert sunlight, water, and carbon dioxide into glucose and oxygen.",
            "focus": "main idea",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "summary" in payload
    assert "photosynthesis" in payload["summary"].lower()
