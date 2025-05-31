from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_login_page():
    response = client.get("/login.html")
    assert response.status_code == 200

def test_signup_page():
    response = client.get("/signup.html")
    assert response.status_code == 200 