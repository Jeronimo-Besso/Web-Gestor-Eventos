from pydantic import BaseModel
from typing import Optional


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str]


class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        orm_mode = True
