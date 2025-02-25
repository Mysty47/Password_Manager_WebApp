from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Temporary storage of login info

saved_passwords = []
saved_login_info ={"" : ""}

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
    if username in saved_login_info and saved_login_info[username] == password:
        return {"status": "success", "message": "Login successful!"}
    return {"status": "error", "message": "Invalid credentials"}

# After signup

@app.post("/signup/")
async def signup(username: str = Form(...), password: str = Form(...)):
    saved_login_info[username] = password
    return {"status": "success", "message": "Signup successful!"}

# After saving password

@app.post("/save_password/")
async def save_password(name: str = Form(...), password: str = Form(...)):
    saved_passwords.append({"name": name, "password": password})
    return {"status": "success", "message": "Password saved successfully!"}
    
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
    return {"passwords": saved_passwords}