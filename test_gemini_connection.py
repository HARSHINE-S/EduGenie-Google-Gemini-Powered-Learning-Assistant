from fastapi.testclient import TestClient
from main import app


def test_gemini_test_endpoint_returns_response():
    client = TestClient(app)
    response = client.post(
        "/api/gemini-test",
        json={"prompt": "Say hello in one sentence."}
    )

    print("\nSTATUS:", response.status_code)
    print("BODY:", response.text)

    assert response.status_code == 200
