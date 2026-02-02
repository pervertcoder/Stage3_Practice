from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import jwt

app = FastAPI()

@app.post("/insert_message")
def insert_message(request):
    pass

@app.get("/render_message")
def render_message():
    pass

app.mount("/static", StaticFiles(directory="static"))
# Static Pages
@app.get("/")
async def index(request: Request):
    return FileResponse("./static/index.html")