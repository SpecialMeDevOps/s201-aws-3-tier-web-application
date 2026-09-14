import pytest
from app import create_app, db

@pytest.fixture()
def client(tmp_path):
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path}/test.db"})
    with app.test_client() as client:
        yield client

def test_health(client):
    assert client.get("/health").json == {"status": "ok"}

def test_rejects_private_target(client, monkeypatch):
    monkeypatch.setattr("app.validation.socket.getaddrinfo", lambda *a, **k: [(None, None, None, None, ("127.0.0.1", 80))])
    response = client.post("/api/jobs", json={"target_url": "http://localhost"})
    assert response.status_code == 400

def test_creates_job(client, monkeypatch):
    monkeypatch.setattr("app.validation.socket.getaddrinfo", lambda *a, **k: [(None, None, None, None, ("93.184.216.34", 80))])
    response = client.post("/api/jobs", json={"target_url": "https://example.com"})
    assert response.status_code == 202
    assert response.json["status"] == "queued"
