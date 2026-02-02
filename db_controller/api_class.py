from pydantic import BaseModel
from typing import List

class DataDetail(BaseModel):
    content : str

class DataRequest(BaseModel):
    data : DataDetail

class responseDataDetail(BaseModel):
    msg : list

class responseData(BaseModel):
    data : responseDataDetail

class photoResponseDetail(BaseModel):
    ok : bool

class photoResponse(BaseModel):
    data : photoResponseDetail