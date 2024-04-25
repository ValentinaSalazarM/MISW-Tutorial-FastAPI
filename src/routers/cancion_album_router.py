from fastapi import HTTPException, APIRouter, Depends, status
from  src.db.database import get_db
from sqlalchemy.orm import Session

from src.models.db_models import Cancion, Album
from src.schemas.pydantic_schemas import CancionSchema, CancionAlbumCreateSchema

cancion_album_router = APIRouter(tags=['CanciónÁlbum'])

@cancion_album_router.get('/album/{id_album}/canciones', response_model = list[CancionSchema])
def obtener_canciones_album (id_album: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == id_album).first()
    return album.canciones

@cancion_album_router.post('/album/{id_album}/canciones', response_model = CancionSchema)
def crear_cancion_album(id_album: int, cancion: CancionAlbumCreateSchema, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == id_album).first()

    if cancion.id_cancion is not None:
        db_nueva_cancion = db.query(Cancion).filter(Cancion.id == cancion.id_cancion).first()
        if db_nueva_cancion is not None:
            album.canciones.append(db_nueva_cancion)
            db.commit()
        else:
            return HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Canción no encontrada.')
    else:
        db_nueva_cancion = Cancion(titulo = cancion.titulo, 
                        minutos = cancion.minutos, 
                        segundos = cancion.segundos, 
                        interprete = cancion.interprete)
        album.canciones.append(db_nueva_cancion)
    db.commit()
    return db_nueva_cancion
