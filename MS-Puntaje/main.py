from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import PlainTextResponse
import json

import requests 
app = FastAPI()

@app.get("/")
async def root():
    return "Healthcheck Microservice 1"

@app.post("/cancion/{id_cancion}/puntuar", response_class = PlainTextResponse)
async def puntuar_cancion(id_cancion, puntaje:float = Query (ge = 0, le = 5)):
    content = requests.get('http://127.0.0.1:5000/cancion/{}'.format(id_cancion))
    if content.status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Canción no encontrada.')
    else:
        db_cancion = content.json()
        db_cancion["puntaje"] = float(puntaje)
        return json.dumps(db_cancion)
