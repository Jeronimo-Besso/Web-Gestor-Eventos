from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: Optional[str] = "Cliente"


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
