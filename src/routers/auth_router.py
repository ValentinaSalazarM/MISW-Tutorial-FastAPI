from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse

from src.db.database import get_db
from src.models.db_models import Usuario
from src.schemas.pydantic_schemas import UsuarioCreateSchema, UsuarioLoginSchema, UsuarioSchema

from sqlalchemy.orm import Session

auth_router = APIRouter(tags=['Auth'])

@auth_router.post('/signup', response_model = UsuarioSchema)
async def create_user(user: UsuarioCreateSchema, db: Session = Depends(get_db)):
    db_user_username = db.query(Usuario).filter(Usuario.nombre == user.nombre).first()
    if db_user_username:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'El nombre ya se encuentra registrado.',
        )
    db_user = Usuario(
        nombre = user.nombre,
        contrasena = user.contrasena,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@auth_router.post('/login', response_class = PlainTextResponse)
async def login_for_access_token(user: UsuarioLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(Usuario).filter(Usuario.nombre == user.nombre).first()
    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail = 'El usuario no es correcto.')

    if not user.contrasena == user_db.contrasena:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = 'La contraseña no es correcta.')

    return PlainTextResponse('Inicio de sesión exitoso.', status_code = status.HTTP_200_OK)