from fastapi import APIRouter, HTTPException
from typing import Optional

from app.db.database import get_db_connection
from app.models.password_entry import PasswordEntry

router = APIRouter()

# Store current user (Consider a more robust state management in a real app)
current_user: Optional[str] = None

# Get current user
@router.get("/current_user")
async def get_current_user():
    # Access the global current_user. In a real app, this would involve sessions/tokens.
    from main import current_user # Importing from main for now due to global state
    return {"username": current_user}

# Logout
@router.post("/logout")
async def logout():
    # Modify the global current_user. In a real app, this would involve session/token invalidation.
    from main import current_user
    global current_user
    current_user = None
    return {"status": "success", "message": "Logged out successfully"}

# Saving the password
@router.post("/save_password/")
async def save_password(entry: PasswordEntry):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = connection.cursor()
        # Using the saved_passwords table
        cursor.execute("INSERT INTO login_info.saved_passwords (name, password) VALUES (%s, %s)",
                       (entry.name, entry.password))
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "success", "message": "Password saved successfully!"}
    except mysql.connector.Error as err:
        # Log the detailed database error on the backend
        print(f"Database Error in save_password: {err}")
        raise HTTPException(status_code=500, detail=f"Database error occurred: {err}")

# After saving password
@router.get("/saved_passwords")
async def get_saved_passwords():
    connection = get_db_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    try:
        cursor = connection.cursor(dictionary=True)
        # Using the saved_passwords table
        cursor.execute("SELECT name, password FROM login_info.saved_passwords")
        passwords = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"passwords": passwords}
    except mysql.connector.Error as err:
        # Log the detailed database error on the backend
        print(f"Database Error in get_saved_passwords: {err}")
        return {"status": "error", "message": "Database error fetching passwords."} 