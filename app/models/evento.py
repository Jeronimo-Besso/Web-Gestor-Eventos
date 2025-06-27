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

    def inscribir(self):
        if self.cupos and self.cupos > 0:
            # print("cupos antes de inscripcion", self.cupos)
            self.cupos -= 1
            # print("cupos despues de inscripcion", self.cupos)
        else:
            raise ValueError("No hay cupos disponibles para este evento.")

    def desinscribir(self):
        # no debo hacer validacion para esto, porque si YA esta inscripto hay cupon para desinscribirse
        # print("cupos antes de desinscribirse", self.cupos)
        self.cupos += 1
        # print("cuppos despues de desinscribirse", self.cupos)
