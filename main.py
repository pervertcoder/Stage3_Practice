from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from db_controller.sql_controller import write_message, get_message, delete
from db_controller.api_class import DataRequest, responseData, photoResponse, deleteAll
import shutil
import os
import glob

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
    path = f"uploads/{file.filename}"
    with open (path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print(path)
    return {
        "data" : {
            "ok" : True,
            "path" : path
        }
    }

@app.delete("/api/delete", response_model=deleteAll)
def delete_all():
    delete()
    folder_path = "uploads"
    files = glob.glob(os.path.join(folder_path, "*.JPG"))
    for f in files:
        os.remove(f)
        print("deleted")
    return {
        "ok" : True
    }

app.mount("/static", StaticFiles(directory="static"))
app.mount("/uploads", StaticFiles(directory="uploads"))
# Static Pages
@app.get("/")
async def index(request: Request):
    return FileResponse("./static/index.html")