SETUP:


pip install poetry


poetry install


cd app


uvicorn fastapi_server:app --host 127.0.0.1 --port 9999


Queryes:

GET:
http://localhost:9999/sensors
http://localhost:9999/sensors/14
http://localhost:9999/sensors/14/param

POST:
http://localhost:9999/sensors/create
{
    "description": "description",
    "qty": 1
}

Добавление параметров сенсору
http://localhost:9999/sensors/14/param
{   
    "param": 6
}

DELETE:
http://localhost:9999/sensors/4

Изменить данные сенсора
PUT:
http://localhost:9999/sensors/14
{   
    "description": "VIT",
    "qty": 3
}

