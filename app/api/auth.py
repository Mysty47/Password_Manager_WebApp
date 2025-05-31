from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.db.database import get_db_connection

router = APIRouter()

# Assuming you have Jinja2Templates instance available, perhaps passed or imported
# templates = Jinja2Templates(directory="app/templates") 

# Temporary storage of login info (Consider replacing with database interaction)
saved_login_info ={"" : ""}

# After login
@router.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    connection = get_db_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()
    # Using the webappdb table for login
    cursor.execute("SELECT password FROM login_info.webappdb WHERE username = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result and result[0] == password:
        # In a real app, you'd handle sessions or tokens here
        # For simplicity based on the original code, we might update a global state or similar,
        # but that's not scalable. Let's return success.
        return {"status": "success", "message": "Login successful!", "username": username}
    return {"status": "error", "message": "Invalid credentials"}

# After signup
@router.post("/signup/")
async def signup(username: str = Form(...), password: str = Form(...)):
    connection = get_db_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()
    # Using the webappdb table for signup
    cursor.execute("INSERT INTO login_info.webappdb (username, password) VALUES (%s, %s)", (username, password))
    connection.commit()

    cursor.close()
    connection.close()

    return {"status": "success", "message": "Signup successful!"} 