from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from db_controller.sql_controller import write_message, get_message
from db_controller.api_class import DataRequest, responseData, photoResponse
import shutil

app = FastAPI()

@app.post("/api/insert")
def insert_message(request:DataRequest):
    msg = request.data.content
    write_message(msg)
    
    return {
        "data" : {
        "ok" : True
        }
    }

@app.get("/api/render", response_model=responseData)
def render_message():
    result = get_message()
    print(result)
    
    return {
        "data" : {
            "msg" : result
        }
    }

@app.post("/api/upload", response_model=photoResponse)
def upload_photo(file:UploadFile = File(...)):
    with open (f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "data" : {
            "ok" : True
        }
    }

app.mount("/static", StaticFiles(directory="static"))
# Static Pages
@app.get("/")
async def index(request: Request):
    return FileResponse("./static/index.html")