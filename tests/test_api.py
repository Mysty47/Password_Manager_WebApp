from fastapi.testclient import TestClient
from main import app
import unittest.mock
import pytest
import mysql.connector
from mysql.connector.cursor_cext import CMySQLCursorDict # Import the specific class for type hinting/mock spec

# Import the actual get_db dependency
from app.db.database import get_db

# Create a pytest fixture for the test client with dependency overrides
@pytest.fixture
def test_app_and_mocks():
    # Setup: Create mock connection and cursor
    mock_conn = unittest.mock.Mock()
    mock_cursor = unittest.mock.Mock()
    mock_conn.cursor.return_value = mock_cursor

    # Create a function that the dependency override will call
    def override_get_db():
        yield mock_conn

    # Override the actual get_db dependency with our mock function
    app.dependency_overrides[get_db] = override_get_db

    # Yield both the TestClient and the mocks
    yield TestClient(app), mock_conn, mock_cursor

    # Teardown: Remove the dependency override after the test finishes
    app.dependency_overrides = {}

# Now, update the tests to use the fixture

def test_read_root(test_app_and_mocks):
    client, _, _ = test_app_and_mocks # We only need the client for this test
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']

def test_signup_with_mocks(test_app_and_mocks):
    client, mock_conn, mock_cursor = test_app_and_mocks

    response = client.post("/signup/", data={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Signup successful!"}

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("INSERT INTO login_info.webappdb (username, password) VALUES (%s, %s)", ("testuser", "testpassword"))
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_login_success_with_mocks(test_app_and_mocks):
    client, mock_conn, mock_cursor = test_app_and_mocks

    mock_cursor.fetchone.return_value = ("testpassword",)

    response = client.post("/login/", data={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Login successful!", "username": "testuser"}

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT password FROM login_info.webappdb WHERE username = %s", ("testuser",))
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_login_fail_password_with_mocks(test_app_and_mocks):
    client, mock_conn, mock_cursor = test_app_and_mocks

    mock_cursor.fetchone.return_value = ("wrongpassword",)

    response = client.post("/login/", data={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {"status": "error", "message": "Invalid credentials"}

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT password FROM login_info.webappdb WHERE username = %s", ("testuser",))
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_login_fail_user_with_mocks(test_app_and_mocks):
    client, mock_conn, mock_cursor = test_app_and_mocks

    mock_cursor.fetchone.return_value = None

    response = client.post("/login/", data={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {"status": "error", "message": "Invalid credentials"}

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT password FROM login_info.webappdb WHERE username = %s", ("testuser",))
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_save_password_with_mocks(test_app_and_mocks):
    client, mock_conn, mock_cursor = test_app_and_mocks

    response = client.post("/save_password/", json={
        "name": "testsite",
        "password": "sitepassword"
    })

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Password saved successfully!"}

    # The endpoint calls cursor() without dictionary=True for saving
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("INSERT INTO login_info.saved_passwords (name, password) VALUES (%s, %s)", ("testsite", "sitepassword"))
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_get_saved_passwords_with_mocks(test_app_and_mocks):
    client, mock_conn, mock_cursor = test_app_and_mocks

    # Configure cursor to be dictionary=True as in the original code
    # The mock_conn.cursor.return_value is already set, just need to configure the returned mock_cursor
    mock_cursor.configure_mock(spec_set=CMySQLCursorDict)

    # Simulate the database returning some saved passwords
    mock_cursor.fetchall.return_value = [
        {"name": "site1", "password": "pass1"},
        {"name": "site2", "password": "pass2"}
    ]

    response = client.get("/saved_passwords")

    assert response.status_code == 200
    assert response.json() == {"passwords": [
        {"name": "site1", "password": "pass1"},
        {"name": "site2", "password": "pass2"}
    ]}

    # The endpoint calls cursor() with dictionary=True for fetching
    mock_conn.cursor.assert_called_once_with(dictionary=True)
    mock_cursor.execute.assert_called_once_with("SELECT name, password FROM login_info.saved_passwords")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once() 