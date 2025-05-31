from fastapi.testclient import TestClient
from main import app
import unittest.mock
import pytest
import mysql.connector
from mysql.connector.cursor_cext import CMySQLCursorDict # Import the specific class for type hinting/mock spec
import bcrypt
import os
from cryptography.fernet import Fernet
from unittest.mock import patch, MagicMock, call # Remove PropertyMock import
from fastapi.templating import Jinja2Templates

# Import the actual get_db dependency
from app.db.database import get_db
# Import the actual modules and variables we need to modify
import main # Import the main module to access globals directly
from app.api.auth import user_encryption_keys # Import the dictionary

# Create a test templates directory
templates = Jinja2Templates(directory="app/templates")

# Create a pytest fixture for the test client with dependency overrides and module mocks
@pytest.fixture
def test_app_and_mocks():
    # Mock the get_db_connection function from app.db.database
    with patch('app.db.database.get_db_connection') as mock_get_db_connection:
        # Create mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # Configure the mock connection to return the mock cursor
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Configure the FastAPI app to use the mocked dependency
        app.dependency_overrides[get_db] = lambda: mock_conn

        # Store original values to restore later
        original_current_user = main.current_user
        original_current_user_id = main.current_user_id
        original_user_encryption_keys = user_encryption_keys.copy()

        # Patch the encryption keys dictionary
        with patch.dict('app.api.auth.user_encryption_keys', {}, clear=True) as mock_user_encryption_keys:
            with TestClient(app) as client:
                yield client, mock_conn, mock_cursor, mock_user_encryption_keys

        # Teardown
        app.dependency_overrides = {}
        main.current_user = original_current_user
        main.current_user_id = original_current_user_id
        user_encryption_keys.clear()
        user_encryption_keys.update(original_user_encryption_keys)

def test_read_main(test_app_and_mocks):
    client, mock_conn, mock_cursor, mock_user_encryption_keys = test_app_and_mocks
    response = client.get("/")
    assert response.status_code == 200
    assert "Backend Connected!" in response.text

def test_signup_with_mocks(test_app_and_mocks):
    # The fixture now only yields 4 values
    client, mock_conn, mock_cursor, mock_user_encryption_keys = test_app_and_mocks

    # Mock execute such that the first call (SELECT) returns None (user not exists)
    # and the second call (INSERT) succeeds.
    mock_cursor.execute.side_effect = [None, None] # Simulate SELECT then INSERT
    mock_cursor.fetchone.return_value = None # SELECT returns None

    response = client.post("/signup/", data={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == 200 # Expecting 200 for successful signup
    assert response.json() == {"status": "success", "message": "Signup successful!"}

    # Assert that execute was called twice
    assert mock_cursor.execute.call_count == 2
    # Check the first call (SELECT)
    mock_cursor.execute.assert_any_call("SELECT username FROM login_info.webappdb WHERE username = %s", ("testuser",))
    # Check the second call (INSERT)
    mock_cursor.execute.assert_any_call("INSERT INTO login_info.webappdb (username, password, salt) VALUES (%s, %s, %s)", 
                                      ("testuser", unittest.mock.ANY, unittest.mock.ANY))
    mock_conn.commit.assert_called_once()

def test_login_success_with_mocks(test_app_and_mocks):
    # The fixture now only yields 4 values
    client, mock_conn, mock_cursor, mock_user_encryption_keys = test_app_and_mocks

    # Simulate a stored hashed password and a mock salt for the user
    mock_hashed_password = bcrypt.hashpw(b"testpassword", bcrypt.gensalt())
    mock_salt = os.urandom(16)
    # Mock the first fetchone call (for password and salt)
    mock_cursor.fetchone.side_effect = [(mock_hashed_password.decode('utf-8'), mock_salt), (1,)] # Simulate fetching password/salt then user ID

    # Mock bcrypt.checkpw to return True
    with patch('bcrypt.checkpw', return_value=True):
        response = client.post("/login/", data={
            "username": "testuser",
            "password": "testpassword"
        })

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Login successful!", "username": "testuser"}

    # Assert that the global variables were set correctly
    assert main.current_user == "testuser"
    assert main.current_user_id == 1
    # Assert that an encryption key was stored for the user in the patched dictionary
    assert "testuser" in mock_user_encryption_keys
    assert isinstance(mock_user_encryption_keys["testuser"], Fernet)

    # Assert execute was called twice (select password/salt, select user ID)
    assert mock_cursor.execute.call_count == 2
    mock_cursor.execute.assert_any_call("SELECT password, salt FROM login_info.webappdb WHERE username = %s", ("testuser",))
    mock_cursor.execute.assert_any_call("SELECT id FROM login_info.webappdb WHERE username = %s", ("testuser",))

def test_login_fail_password_with_mocks(test_app_and_mocks):
    # The fixture now only yields 4 values
    client, mock_conn, mock_cursor, mock_user_encryption_keys = test_app_and_mocks

    # Simulate a stored wrong hashed password and a mock salt
    mock_hashed_password = bcrypt.hashpw(b"wrongpassword", bcrypt.gensalt())
    mock_salt = os.urandom(16)
    # Mock the first fetchone call (for password and salt)
    mock_cursor.fetchone.return_value = (mock_hashed_password.decode('utf-8'), mock_salt)

    # Mock bcrypt.checkpw to return False
    with patch('bcrypt.checkpw', return_value=False):
        response = client.post("/login/", data={
            "username": "testuser",
            "password": "testpassword"
        })

    assert response.status_code == 200 # The endpoint returns 200 with an error message
    assert response.json() == {"status": "error", "message": "Invalid credentials"}

    # Assert that the global variables were NOT set
    assert main.current_user is None
    assert main.current_user_id is None
    assert "testuser" not in mock_user_encryption_keys # Check the patched dictionary

    mock_cursor.execute.assert_called_once_with("SELECT password, salt FROM login_info.webappdb WHERE username = %s", ("testuser",))

def test_login_fail_user_with_mocks(test_app_and_mocks):
    # The fixture now only yields 4 values
    client, mock_conn, mock_cursor, mock_user_encryption_keys = test_app_and_mocks

    # Simulate user not found (first fetchone returns None)
    mock_cursor.fetchone.return_value = None

    response = client.post("/login/", data={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == 200 # The endpoint returns 200 with an error message
    assert response.json() == {"status": "error", "message": "Invalid credentials"}

    # Assert that the global variables were NOT set
    assert main.current_user is None
    assert main.current_user_id is None
    assert "testuser" not in mock_user_encryption_keys # Check the patched dictionary

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT password, salt FROM login_info.webappdb WHERE username = %s", ("testuser",))

def test_save_password_with_mocks(test_app_and_mocks):
    # The fixture now only yields 4 values
    client, mock_conn, mock_cursor, mock_user_encryption_keys = test_app_and_mocks

    # Simulate a logged-in user by setting the global variables directly
    main.current_user = "testuser"
    main.current_user_id = 1
    # Simulate a Fernet key and add it to the patched dictionary
    encryption_key = Fernet.generate_key()
    fernet_instance = Fernet(encryption_key)
    mock_user_encryption_keys["testuser"] = fernet_instance # Add to the patched dictionary

    # Mock the cursor execute to succeed for the insert
    mock_cursor.execute.side_effect = None # Ensure no side effect from previous tests
    mock_conn.commit.side_effect = None # Ensure no side effect from previous tests

    response = client.post("/save_password/", json={
        "name": "testsite",
        "password": "sitepassword"
    })

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Password saved successfully!"}

    # Assert that execute was called to insert the password entry with user_id
    mock_cursor.execute.assert_called_once_with("INSERT INTO login_info.saved_passwords (user_id, name, password) VALUES (%s, %s, %s)",
                                              (1, unittest.mock.ANY, unittest.mock.ANY))
    mock_conn.commit.assert_called_once()

def test_get_saved_passwords_with_mocks(test_app_and_mocks):
    # The fixture now only yields 4 values
    client, mock_conn, mock_cursor, mock_user_encryption_keys = test_app_and_mocks

    # Simulate a logged-in user by setting the global variables directly
    main.current_user = "testuser"
    main.current_user_id = 1
    # Simulate a Fernet key for decryption and add it to the patched dictionary
    encryption_key = Fernet.generate_key()
    fernet_instance = Fernet(encryption_key)
    mock_user_encryption_keys["testuser"] = fernet_instance # Add to the patched dictionary

    # Simulate encrypted data returned from the database
    encrypted_name1 = fernet_instance.encrypt(b"site1")
    encrypted_password1 = fernet_instance.encrypt(b"pass1")
    encrypted_name2 = fernet_instance.encrypt(b"site2")
    encrypted_password2 = fernet_instance.encrypt(b"pass2")

    # Mock the cursor to return the encrypted data
    mock_cursor.fetchall.return_value = [
        (encrypted_name1, encrypted_password1),
        (encrypted_name2, encrypted_password2)
    ]

    response = client.get("/saved_passwords")

    assert response.status_code == 200
    # The expected response should contain decrypted data
    assert response.json() == {"passwords": [
        {"name": "site1", "password": "pass1"},
        {"name": "site2", "password": "pass2"}
    ]}

    # Assert that execute was called to select passwords for the current user
    mock_cursor.execute.assert_called_once_with("SELECT name, password FROM login_info.saved_passwords WHERE user_id = %s", (1,)) 