from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    message = "Backend test"
    return templates.TemplateResponse("login.html", {"request": request, "message": message})

@app.get("/login.html", response_class=HTMLResponse)
async def read_root(request: Request):
    message = "Backend test"
    return templates.TemplateResponse("login.html", {"request": request, "message": message})
