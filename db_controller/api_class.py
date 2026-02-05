from pydantic import BaseModel
from typing import List

class DataDetail(BaseModel):
    content : str

class DataRequest(BaseModel):
    data : DataDetail

class responseDataDetail(BaseModel):
    msg : list
    path : list

class responseData(BaseModel):
    data : responseDataDetail

class photoResponseDetail(BaseModel):
    ok : bool
    path : list

class photoResponse(BaseModel):
    data : photoResponseDetail

class deleteAll(BaseModel):
    ok : bool

class deleteRequestDetail(BaseModel):
    localArr : list

class deleteRequest(BaseModel):
    data : deleteRequestDetail