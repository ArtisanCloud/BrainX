from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_system_status():
    response = client.get("/api/system/status")
    assert response.status_code == 200
    assert response.json() == {
        "system": True,
        "version": "0.0.5",
        "WorkerCount": 1,
        "OllamaUrl": "http://localhost:11434"
    }
