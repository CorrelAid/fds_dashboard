from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    temp = response.json()
    assert "foi_requests" in temp
