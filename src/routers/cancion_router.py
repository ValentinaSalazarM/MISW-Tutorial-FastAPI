from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from src.db.database import get_db
from sqlalchemy.orm import Session

from src.models.db_models import Cancion
from src.schemas.pydantic_schemas import CancionSchema, CancionCreateUpdateSchema

cancion_router = APIRouter(tags=['Canción'])

@cancion_router.get('/canciones', response_model = list[CancionSchema])
def listado_canciones(db: Session= Depends(get_db)):
    return db.query(Cancion).all()

@cancion_router.get('/cancion/{id_cancion}', response_model = CancionSchema)
def obtener_cancion (id_cancion: int, db: Session = Depends(get_db)):
    db_cancion = db.query(Cancion).filter(Cancion.id == id_cancion).first()
    if db_cancion is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = 'Canción no encontrada.')
    return db_cancion

@cancion_router.post('/canciones')
def crear_cancion(cancion: CancionCreateUpdateSchema, db: Session = Depends(get_db)):
    db_cancion = Cancion(titulo = cancion.titulo, 
                      minutos = cancion.minutos, 
                      segundos = cancion.segundos, 
                      interprete = cancion.interprete)
    db.add(db_cancion)
    db.commit()
    db.refresh(db_cancion)
    return db_cancion

@cancion_router.put('/cancion/{id_cancion}', response_model = CancionSchema)
def actualizar_cancion (id_cancion: int, cancion_update: CancionCreateUpdateSchema, db: Session = Depends(get_db)):
    db_cancion = db.query(Cancion).filter(Cancion.id == id_cancion)
    db_cancion.first()
    if db_cancion == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Canción no encontrada.')
    else:
        db_cancion.update(cancion_update.model_dump())
        db.commit()
    return db_cancion.first()
    
@cancion_router.delete('/cancion/{id_cancion}', response_class = PlainTextResponse)
def eliminar_cancion(id_cancion: int, db: Session = Depends(get_db)):
    db_cancion = db.query(Cancion).filter(Cancion.id == id_cancion).first()
    db.delete(db_cancion)
    db.commit()
    return PlainTextResponse('Canción eliminada.', status_code = status.HTTP_200_OK)


