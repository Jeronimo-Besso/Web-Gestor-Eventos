from pydantic import BaseModel
from datetime import date
from typing import Optional

class EventoBase(BaseModel):
    nombre: str
    descripcion: Optional[str]
    fecha_inicio: date
    fecha_fin: date
    lugar: str
    cupos: int
    categoria_id: int

class EventoCreate(EventoBase):
    pass

class EventoResponse(EventoBase):
    id: int

    class Config:
        orm_mode = True