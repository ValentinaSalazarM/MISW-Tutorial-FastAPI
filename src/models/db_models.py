from sqlalchemy import Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship
from src.db.database import Base
import enum

albumes_canciones = Table('album_cancion', Base.metadata,
    Column('album_id', Integer, ForeignKey('albumes.id'), primary_key = True),
    Column('cancion_id', Integer, ForeignKey('canciones.id'), primary_key = True))

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    contrasena = Column(String(50))
    albumes = relationship('Album', back_populates='propietario')

class Album(Base):
    __tablename__ = 'albumes'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(128))
    anio = Column(Integer)
    descripcion = Column(String(512))
    medio = Column(String(512))
    propietario_id = Column(Integer, ForeignKey('usuarios.id'))
    propietario = relationship('Usuario', back_populates='albumes')
    canciones = relationship('Cancion', secondary = 'album_cancion', back_populates='albumes')
    
class Cancion(Base):
    __tablename__ = 'canciones'
    id = Column(Integer, primary_key = True)
    titulo = Column(String(128))
    minutos = Column(Integer)
    segundos = Column(Integer)
    interprete = Column(String(128))
    albumes = relationship('Album', secondary = 'album_cancion', back_populates='canciones')
