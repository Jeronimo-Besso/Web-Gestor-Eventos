from pydantic import BaseModel
from datetime import date


# Modelo para recibir datos cuando el usuario se inscribe
class InscripcionCreate(BaseModel):
    evento_id: int


# Modelo base del evento (usado dentro de respuestas)
class EventoResponse(BaseModel):
    id: int
    nombre: str
    fecha_inicio: date
    fecha_fin: date

    class Config:
        from_attributes = True


# Respuesta del POST: inscripción simple, sin datos del evento
class InscripcionResponse(BaseModel):
    id: int
    evento_id: int
    fecha_inscripcion: date

    class Config:
        from_attributes = True


# Respuesta para GETs enriquecidos: incluye el objeto evento completo
class InscripcionConEventoResponse(BaseModel):
    id: int
    fecha_inscripcion: date
    evento: EventoResponse

    class Config:
        from_attributes = True
