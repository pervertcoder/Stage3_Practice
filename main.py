from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from db_controller.sql_controller import write_message, get_message, delete
from db_controller.api_class import DataRequest, responseData, photoResponse, deleteAll
from funcDef.functiondef import time_process, file_name_process
import boto3

s3 = boto3.resource("s3")
app = FastAPI()

bucket = s3.Bucket("test-photo-pervertclouder")
cloud_front_url = "https://df77blnctku6q.cloudfront.net/"

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
    path_processing = sorted(bucket.objects.filter(Prefix="images/"), key=lambda obj:obj.last_modified, reverse=False)
    path = [cloud_front_url + obj.key for obj in path_processing]
    result = get_message()
    # print(result)
    
    return {
        "data" : {
            "msg" : result,
            "path" : path
        }
    }


@app.post("/api/upload", response_model=photoResponse)
def upload_photo(file:UploadFile = File(...)):
    time = time_process()
    file1 = file.filename
    file_name_done = file_name_process(file1, time)
    photo_cloudfront = f"images/{file_name_done}"
    s3.Bucket("test-photo-pervertclouder").put_object(Key = photo_cloudfront, Body = file.file)
    return {
        "data" : {
            "ok" : True
        }
    }

def data_process(path:list) -> list:
    targetArr = []
    for i in path:
        target_son = i[37:]
        targetArr.append(target_son)
    return targetArr

@app.delete("/api/delete", response_model=deleteAll)
def delete_all():
    path = [cloud_front_url + obj.key for obj in bucket.objects.filter(Prefix="images/")]
    delete()
    data = data_process(path)
    dataArr = []
    for i in range(len(data)):
        dataArr.append({"Key" : f"{data[i]}"})
    
    s3.Bucket("test-photo-pervertclouder").delete_objects(Delete = {
        "Objects" : dataArr
    })
    return {
        "ok" : True
    }

# app.mount("/static", StaticFiles(directory="static"))
# # Static Pages
# @app.get("/")
# async def index(request: Request):
#     return FileResponse("./static/index.html")