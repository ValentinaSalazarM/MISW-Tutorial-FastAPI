from fastapi import FastAPI

from src.models import db_models
from src.routers.album_router import album_router
from src.routers.album_usuario_router import album_usuario_router
from src.routers.auth_router import auth_router
from src.routers.cancion_album_router import cancion_album_router
from src.routers.cancion_router import cancion_router

from src.db.database import engine

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return "Healthcheck"

app.include_router(router = album_router)
app.include_router(router = album_usuario_router)
app.include_router(router = auth_router)
app.include_router(router = cancion_album_router)
app.include_router(router = cancion_router)
