from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from src.db.database import get_db
from sqlalchemy.orm import Session

from src.models.db_models import Usuario, Album
from src.schemas.pydantic_schemas import AlbumSchema, AlbumCreateUpdateSchema

album_usuario_router = APIRouter(tags=['ÁlbumUsuario'])

@album_usuario_router.get('/usuario/{id_propietario}/albumes', response_model = list[AlbumSchema])
def obtener_albumes_usuario (id_propietario: int, 
                             db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id_propietario).first()
    return usuario.albumes

@album_usuario_router.post('/usuario/{id_propietario}/albumes', response_model = AlbumSchema)
def crear_album_usuario (id_propietario: int, 
                         album: AlbumCreateUpdateSchema, 
                         db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id_propietario).first()
    db_album = Album(titulo = album.titulo, 
                      anio = album.anio, 
                      descripcion = album.descripcion, 
                      medio = album.medio)
    usuario.albumes.append(db_album)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return 'El usuario ya tiene un album con dicho nombre', 409
    
    return db_album
