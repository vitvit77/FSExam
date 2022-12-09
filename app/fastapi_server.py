from fastapi import FastAPI, Query
from pydantic import BaseModel
from starlette.responses import JSONResponse

import db

db = db.Database()

app = FastAPI()


class CreateSensorModel(BaseModel):
    description: str
    qty: int

class CreateSensorParamModel(BaseModel):
    param: float|int

class updateSensorModel(BaseModel):
    description: str
    qty: int

class deleteSensorModel(BaseModel):
    id: int


@app.get("/")
def read_root():
    return {"Service": "Sensor"}


@app.get("/sensors/{item_id}")
def read_sensors_id(item_id: int):
    return JSONResponse(status_code=200, content=db.getSensorById(item_id))

@app.get("/sensors", description='This reads an item')
def read_sensors():
    return JSONResponse(status_code=200, content=db.getAllSensors())

@app.post("/sensors/{item_id}/param")
def read_sensors_id_values(request: CreateSensorParamModel, item_id: int):
    return JSONResponse(status_code=200, content={"response": db.createParamSensorInfo(item_id, request.param)})

@app.get("/sensors/{item_id}/param")
def read_sensors_id_values_param(item_id: int):
    return JSONResponse(status_code=200, content=db.getSensorInfoById(item_id))


@app.put("/sensors/{item_id}")
def read_sensors_update(request: updateSensorModel, item_id: int):
    return JSONResponse(status_code=200, content={"response": db.updateSensor(item_id, request.description, request.qty)})

@app.delete("/sensors/{item_id}")
def read_sensors_delete(item_id: int):
    return JSONResponse(status_code=200, content={"response": db.deleteSensorById(item_id)})

@app.post("/sensors/create")
def post_item(request: CreateSensorModel):
    result = db.createSensor(request.description, request.qty)
    return JSONResponse(status_code=200, content={"response": result})
