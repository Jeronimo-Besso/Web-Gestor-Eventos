from pydantic import BaseModel
from datetime import date
from typing import Optional


class CategoriaRespose(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class EventoBase(BaseModel):
    nombre: str
    descripcion: Optional[str]
    fecha_inicio: date
    fecha_fin: date
    lugar: str
    cupos: int
    categoria_id: Optional[int]
    # categoria: Optional[CategoriaRespose]


class EventoCreate(EventoBase):
    pass


class EventoResponse(EventoBase):
    id: int

    class Config:
        from_attributes = True
