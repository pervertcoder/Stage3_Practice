from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from db_controller.sql_controller import write_message, get_message, delete
from db_controller.api_class import DataRequest, responseData, photoResponse, deleteAll, deleteRequest
import boto3

s3 = boto3.resource("s3")
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
    # print(result)
    
    return {
        "data" : {
            "msg" : result
        }
    }

@app.post("/api/upload", response_model=photoResponse)
def upload_photo(file:UploadFile = File(...)):
    cloud_front_url = "df77blnctku6q.cloudfront.net/"
    photo_cloudfront = f"images/{file.filename}"
    s3.Bucket("test-photo-pervertclouder").put_object(Key = photo_cloudfront, Body = file.file)
    return {
        "data" : {
            "ok" : True,
            "path" : "https://" + cloud_front_url + photo_cloudfront
        }
    }


def data_process(arr:list) -> list:
    targetArr = []
    for i in arr:
        target_son = i[37:]
        targetArr.append(target_son)
    return targetArr

@app.post("/api/delete", response_model=deleteAll)
def delete_all(request:deleteRequest):
    delete()
    data = data_process(request.data.localArr)
    dataArr = []
    for i in range(len(data)):
        dataArr.append({"Key" : f"{data[i]}"})
    
    # 比對資料
    # print(dataArr)
    # for obj in s3.Bucket("test-photo-pervertclouder").objects.all():
    #     print(obj.key)
    
    s3.Bucket("test-photo-pervertclouder").delete_objects(Delete = {
        "Objects" : dataArr
    })
    return {
        "ok" : True
    }

app.mount("/static", StaticFiles(directory="static"))
# Static Pages
@app.get("/")
async def index(request: Request):
    return FileResponse("./static/index.html")