from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)  # nombre con límite
    email = Column(String(150), unique=True, nullable=False)  # email largo y único
    hashed_password = Column(String(255), nullable=False)  # hash de contraseña
    rol = Column(String(50), default="Cliente")  # rol corto

    inscripciones = relationship("Inscripcion", back_populates="usuario")
