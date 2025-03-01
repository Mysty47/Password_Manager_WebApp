from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

class PasswordEntry(BaseModel):
    name: str
    password: str

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Database connection

def get_db_connection():
    try:
        connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="parola1",
        database="login_info"
        )
        return connection
    except mysql.connector.Error as err:
        print("Database Connection Error:", err)
        return None



# Temporary storage of login info

# saved_passwords = []
# saved_login_info ={"" : ""}

# Enable CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# After login

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    connection = get_db_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()
    cursor.execute("SELECT password FROM login_info.webappdb WHERE username = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result and result[0] == password:
        return {"status": "success", "message": "Login successful!"}
    return {"status": "error", "message": "Invalid credentials"}



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
    
# Home page

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    message = "Backend Connected!"
    return templates.TemplateResponse("home.html", {"request": request, "message": message})

# Login Page

@app.get("/login.html", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Signup Page

@app.get("/signup.html", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Saved Passwords

@app.get("/saved_passwords")
async def get_saved_passwords():
    connection = get_db_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, password FROM saved_passwords")
    passwords = cursor.fetchall()

    cursor.close()
    connection.close()

    return {"passwords": passwords}
