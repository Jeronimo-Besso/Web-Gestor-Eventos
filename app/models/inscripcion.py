from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base


class Inscripcion(Base):
    __tablename__ = "inscripciones"

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id", ondelete="SET NULL"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_inscripcion = Column(Date, nullable=False)

    evento_nombre = Column(String(100))
    evento_fecha_inicio = Column(Date)
    evento_fecha_fin = Column(Date)

    usuario = relationship("Usuario", back_populates="inscripciones")
    evento = relationship("Evento", back_populates="inscripciones", lazy="joined", foreign_keys=[evento_id])
