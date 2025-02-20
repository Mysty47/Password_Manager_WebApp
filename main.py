from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

templates = Jinja2Templates(directory="app/")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    message = "Backend test"
    return templates.TemplateResponse("home.html", {"request": request, "message": message})
