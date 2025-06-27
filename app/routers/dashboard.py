from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import date
from app.database import get_db
from app.models.evento import Evento
from app.models.inscripcion import Inscripcion
from app.utils.dependencies import require_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/total-eventos")
def total_eventos(db: Session = Depends(get_db), _=Depends(require_admin)):
    return {"total_eventos": db.query(Evento).count()}


@router.get("/inscripciones-activas")
def total_inscripciones_activas(
    db: Session = Depends(get_db), _=Depends(require_admin)
):
    hoy = date.today()
    total = db.query(Inscripcion).join(Evento).filter(Evento.fecha_fin >= hoy).count()
    return {"inscripciones_activas": total}


@router.get("/promedio-inscriptos")
def promedio_inscriptos(db: Session = Depends(get_db), _=Depends(require_admin)):
    total_eventos = db.query(Evento).count()
    total_inscriptos = db.query(Inscripcion).count()
    promedio = total_inscriptos / total_eventos if total_eventos else 0
    return {"promedio_inscriptos_por_evento": round(promedio, 2)}


@router.get("/evento-mas-inscripciones")
def evento_mas_inscripciones(db: Session = Depends(get_db), _=Depends(require_admin)):
    resultado = (
        db.query(Inscripcion.evento_id, func.count(Inscripcion.id).label("cantidad"))
        .group_by(Inscripcion.evento_id)
        .order_by(func.count(Inscripcion.id).desc())
        .first()
    )
    if resultado:
        evento = db.query(Evento).filter(Evento.id == resultado.evento_id).first()
        return {
            "evento_id": evento.id,
            "nombre": evento.nombre,
            "inscripciones": resultado.cantidad,
        }
    return {"mensaje": "No hay inscripciones registradas"}
