from fastapi.testclient import TestClient
from fastapi.templating import Jinja2Templates
from main import app
import pytest
from pathlib import Path
import os

# Get the absolute path to the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

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