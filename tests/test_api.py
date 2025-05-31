from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # We expect HTML content for the root endpoint
    assert "text/html" in response.headers['content-type'] 