from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from app.db.database import get_db_connection, get_db
from app.models.password_entry import PasswordEntry

# Import the temporary key storage and Fernet
from app.api.auth import user_encryption_keys
from cryptography.fernet import Fernet

router = APIRouter()

# Store current user (Consider a more robust state management in a real app)
# current_user: Optional[str] = None # This is now managed in main.py

# Get current user (might need to adjust if user state isn't global)
@router.get("/current_user")
async def get_current_user():
    # Access the global current_user. In a real app, this would involve sessions/tokens.
    from main import current_user # Importing from main for now due to global state
    return {"username": current_user}

# Logout (might need to adjust if user state isn't global)
@router.post("/logout")
async def logout():
    # Modify the global current_user. In a real app, this would involve session/token invalidation.
    from main import current_user
    global current_user

    # Invalidate the encryption key on logout
    if current_user in user_encryption_keys:
        del user_encryption_keys[current_user]

    current_user = None
    return {"status": "success", "message": "Logged out successfully"}

# Saving the password
@router.post("/save_password/")
async def save_password(entry: PasswordEntry, connection = Depends(get_db)):
    from main import current_user, current_user_id # Access current user and user ID
    from app.api.auth import user_encryption_keys # Access the temporary key storage

    print(f"Save password attempt. Current user: {current_user}. Current user ID: {current_user_id}. Key available: {current_user in user_encryption_keys}") # Log check

    if not current_user or current_user not in user_encryption_keys or current_user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated or encryption key/user ID not available.")

    fernet: Fernet = user_encryption_keys[current_user]

    # Encrypt name and password
    encrypted_name = fernet.encrypt(entry.name.encode('utf-8'))
    encrypted_password = fernet.encrypt(entry.password.encode('utf-8'))

    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = connection.cursor()
        # Using the saved_passwords table, insert with user ID
        cursor.execute("INSERT INTO login_info.saved_passwords (user_id, name, password) VALUES (%s, %s, %s)",
                       (current_user_id, encrypted_name, encrypted_password))
        connection.commit()
        cursor.close()
        # connection.close() # Connection is closed by the dependency's finally block
        return {"status": "success", "message": "Password saved successfully!"}
    except mysql.connector.Error as err:
        # Log the detailed database error on the backend
        print(f"Database Error in save_password: {err}")
        raise HTTPException(status_code=500, detail=f"Database error occurred: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during save_password: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during saving password.")

# After saving password
@router.get("/saved_passwords")
async def get_saved_passwords(connection = Depends(get_db)):
    from main import current_user, current_user_id # Access current user and user ID
    from app.api.auth import user_encryption_keys # Access the temporary key storage

    print(f"Fetching passwords for user: {current_user}. User ID: {current_user_id}. Key available: {current_user in user_encryption_keys}") # Log check

    if not current_user or current_user not in user_encryption_keys or current_user_id is None:
        return {"passwords": []} # Return empty list if not authenticated or key/user ID missing

    fernet: Fernet = user_encryption_keys[current_user]

    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    try:
        cursor = connection.cursor()
        # Using the saved_passwords table, select only for the current user
        cursor.execute("SELECT name, password FROM login_info.saved_passwords WHERE user_id = %s", (current_user_id,))
        results = cursor.fetchall()

        decrypted_passwords = []
        for row in results:
            encrypted_name = row[0]
            encrypted_password = row[1]
            try:
                # Decrypt name and password
                decrypted_name = fernet.decrypt(encrypted_name).decode('utf-8')
                decrypted_password = fernet.decrypt(encrypted_password).decode('utf-8')
                decrypted_passwords.append({"name": decrypted_name, "password": decrypted_password})
            except Exception as e:
                print(f"Error decrypting password entry: {e}")
                # Optionally, handle decryption errors (e.g., corrupted data)
                continue # Skip this entry or handle as needed

        cursor.close()
        # connection.close() # Connection is closed by the dependency's finally block

        return {"passwords": decrypted_passwords}
    except mysql.connector.Error as err:
        # Log the detailed database error on the backend
        print(f"Database Error in get_saved_passwords: {err}")
        return {"status": "error", "message": "Database error fetching passwords."}
    except Exception as e:
        print(f"An unexpected error occurred during get_saved_passwords: {e}")
        return {"status": "error", "message": "An unexpected error occurred during fetching passwords."} 