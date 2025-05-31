from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import mysql.connector
from typing import Optional
import os

# Import the routers
from app.api import auth, passwords

app = FastAPI()

class PasswordEntry(BaseModel):
    name: str
    password: str

# Store current user
current_user: Optional[str] = None
current_user_id: Optional[int] = None

# Declares the static directory 
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "parola1"),
            database=os.getenv("DB_NAME", "login_info")
        )
        return connection
    except mysql.connector.Error as err:
        print("Database Connection Error:", err)
        return None

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(auth.router, tags=["auth"])
app.include_router(passwords.router, tags=["passwords"])

# Home page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    message = "Backend Connected!"
    return templates.TemplateResponse(request, "home.html", {"request": request, "message": message, "current_user": current_user})

# Login Page
@app.get("/login.html", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})

# Signup Page
@app.get("/signup.html", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request, "signup.html", {"request": request})

# After login
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    global current_user
    connection = get_db_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()
    cursor.execute("SELECT password FROM login_info.webappdb WHERE username = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result and result[0] == password:
        current_user = username
        return {"status": "success", "message": "Login successful!", "username": username}
    return {"status": "error", "message": "Invalid credentials"}

# Get current user
@app.get("/current_user")
async def get_current_user():
    return {"username": current_user}

# Logout
@app.post("/logout")
async def logout():
    global current_user
    current_user = None
    return {"status": "success", "message": "Logged out successfully"}

# After signup
@app.post("/signup/")
async def signup(username: str = Form(...), password: str = Form(...)):
    connection = get_db_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()
    cursor.execute("INSERT INTO login_info.webappdb (username, password) VALUES (%s, %s)", (username, password))
    connection.commit()

    cursor.close()
    connection.close()

    return {"status": "success", "message": "Signup successful!"}

# Saving the password
@app.post("/save_password/")
async def save_password(entry: PasswordEntry):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO login_info.saved_passwords (name, password) VALUES (%s, %s)",
                       (entry.name, entry.password))
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "success", "message": "Password saved successfully!"}
    except mysql.connector.Error as err:
        return {"status": "error", "message": str(err)}

# After saving password
@app.get("/saved_passwords")
async def get_saved_passwords():
    connection = get_db_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, password FROM login_info.saved_passwords")
    passwords = cursor.fetchall()

    cursor.close()
    connection.close()

    return {"passwords": passwords}
