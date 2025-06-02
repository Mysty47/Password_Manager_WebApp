from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import mysql.connector
import bcrypt # Import bcrypt
import os # Import os for generating salt
import base64 # Import base64 for encoding/decoding keys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet # Import Fernet for encryption

from app.db.database import get_db_connection, get_db
import main # Move import to the top

router = APIRouter()

# Assuming you have Jinja2Templates instance available, perhaps passed or imported
# templates = Jinja2Templates(directory="app/templates") 

# Temporary storage of derived encryption keys (NOT FOR PRODUCTION)
user_encryption_keys = {}

# After login
@router.post("/login/")
async def login(username: str = Form(...), password: str = Form(...), connection = Depends(get_db)):
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()
    try:
        # Retrieve hashed password and encryption salt
        cursor.execute("SELECT password, salt FROM login_info.webappdb WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            hashed_password = result[0]
            encryption_salt = result[1]

            print(f"Login attempt for user: {username}") # Log the user
            print(f"Retrieved Hashed Password: {hashed_password}") # Log the retrieved hash
            print(f"Retrieved Encryption Salt: {encryption_salt}") # Log the retrieved salt
            print(f"Provided Password (encoded): {password.encode('utf-8')}") # Log the provided password

            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Derive encryption key
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=bytes(encryption_salt), # Convert salt to bytes
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
                user_encryption_keys[username] = Fernet(key) # Store Fernet instance

                # Get the user ID and store it temporarily (along with the key)
                cursor.execute("SELECT id FROM login_info.webappdb WHERE username = %s", (username,))
                user_id_result = cursor.fetchone()
                if user_id_result:
                    user_id = user_id_result[0]
                    # In a real app, store this securely in a session
                    main.current_user = username # Keep username for temporary key lookup
                    main.current_user_id = user_id # Store user ID globally (temporarily)

                return {"status": "success", "message": "Login successful!", "username": username}
            else:
                return {"status": "error", "message": "Invalid credentials"}
        else:
             return {"status": "error", "message": "Invalid credentials"}

    except mysql.connector.Error as err:
        print(f"Database Error during login: {err}")
        return {"status": "error", "message": f"Database error during login: {err}"}
    except ImportError as e:
        print(f"Import Error during login: {e}")
        return {"status": "error", "message": f"Server configuration error: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        return {"status": "error", "message": f"An unexpected error occurred during login: {e}"}
    finally:
        cursor.close()
        # connection.close() # Connection is closed by the dependency's finally block

# After signup
@router.post("/signup/")
async def signup(username: str = Form(...), password: str = Form(...), connection = Depends(get_db)):
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()
    try:
        # Check if username already exists
        cursor.execute("SELECT username FROM login_info.webappdb WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Generate password hash
        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        # Generate salt for encryption key derivation
        encryption_salt = os.urandom(16)

        # Insert new user with hashed password and encryption salt
        cursor.execute("INSERT INTO login_info.webappdb (username, password, salt) VALUES (%s, %s, %s)",
                       (username, hashed_password.decode('utf-8'), encryption_salt))
        connection.commit()

        return {"status": "success", "message": "Signup successful!"}
    except mysql.connector.errors.IntegrityError as err:
        print("Signup error:", err) # Log the error on the backend
        # Although we check above, this catches potential race conditions
        if err.errno == 1062:
             raise HTTPException(status_code=400, detail="Username already exists")
        else:
            raise HTTPException(status_code=500, detail="An error occurred during signup")
    except Exception as e:
        print(f"An unexpected error occurred during signup: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during signup")
    finally:
        cursor.close()
        # connection.close() # Connection is closed by the dependency's finally block 