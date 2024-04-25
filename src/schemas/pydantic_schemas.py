from typing import Optional
from pydantic import Field, BaseModel

class UsuarioBase(BaseModel):
    nombre: str

class UsuarioCreateSchema (UsuarioBase):
    contrasena: str

class UsuarioLoginSchema (UsuarioCreateSchema):
    pass


class AlbumBase (BaseModel):
    titulo: str = Field(max_length = 128) 
    anio: int  
    descripcion: str = Field(max_length = 512) 
    medio: str = Field(max_length = 512) 

class AlbumCreateUpdateSchema (AlbumBase):
    pass


class CancionBase (BaseModel):
    titulo: str = Field(max_length = 128) 
    minutos: int  
    segundos: int  
    interprete: str  = Field(max_length = 128)

class CancionCreateUpdateSchema (CancionBase):
    pass

class CancionAlbumCreateSchema (CancionBase):
    id_cancion: int | None = None


class AlbumSchema(AlbumBase):
    id: int
    propietario_id: int
    canciones: list[CancionBase] = []

    class Config:
        orm_mode = True
        
class UsuarioSchema(UsuarioBase):
    id: int
    albumes: list[AlbumBase] = []

    class Config:
        orm_mode = True

class CancionSchema (CancionBase):
    id: int
    albumes: list[AlbumBase] = []

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    access_token: str
    token_type: str