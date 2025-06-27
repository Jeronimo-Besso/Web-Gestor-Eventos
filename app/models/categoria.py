from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)  # Especificamos longitud
    descripcion = Column(String(255))  # Longitud sugerida para textos breves

    eventos = relationship("Evento", back_populates="categoria")
