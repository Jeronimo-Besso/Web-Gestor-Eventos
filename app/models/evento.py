from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)  # Longitud definida
    descripcion = Column(String(500))  # Texto descriptivo
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    lugar = Column(String(150))  # Lugar del evento
    cupos = Column(Integer)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    categoria = relationship("Categoria", back_populates="eventos")
    inscripciones = relationship("Inscripcion", back_populates="evento")
