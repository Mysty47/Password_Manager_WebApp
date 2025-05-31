from fastapi.testclient import TestClient
from fastapi.templating import Jinja2Templates
from main import app
import pytest
from pathlib import Path

# Create a test templates directory
templates = Jinja2Templates(directory="app/templates")

@pytest.fixture
def client():
    return TestClient(app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Backend Connected!" in response.text

def test_login_page(client):
    response = client.get("/login.html")
    assert response.status_code == 200
    assert "login" in response.text.lower()

def test_signup_page(client):
    response = client.get("/signup.html")
    assert response.status_code == 200
    assert "signup" in response.text.lower() 