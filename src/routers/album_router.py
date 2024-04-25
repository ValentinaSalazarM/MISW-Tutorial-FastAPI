from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from src.schemas.pydantic_schemas import AlbumSchema, AlbumCreateUpdateSchema
from src.db.database import get_db
from src.models.db_models import Album

album_router = APIRouter(tags=['Álbum'])

@album_router.get('/album/{id_album}', response_model = AlbumSchema)
def obtener_album (id_album: int, db: Session = Depends(get_db)):
    db_album = db.query(Album).filter(Album.id == id_album).first()
    if db_album is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Album no encontrado.")
    return db_album

@album_router.put('/album/{id_album}', response_model = AlbumSchema)
def actualizar_album (id_album: int, album_update: AlbumCreateUpdateSchema, db: Session = Depends(get_db)):
    db_album = db.query(Album).filter(Album.id == id_album)
    db_album.first()

    if db_album == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Album no encontrado.")
    else:
        db_album.update(album_update.model_dump())
        db.commit()
    return db_album.first()
    
@album_router.delete('/album/{id_album}', response_class = PlainTextResponse)
def eliminar_album(id_album: int, db: Session = Depends(get_db)):
    db_album = db.query(Album).filter(Album.id == id_album).first()
    db.delete(db_album)
    db.commit()
    return PlainTextResponse('Album eliminado.', status_code = status.HTTP_200_OK)

