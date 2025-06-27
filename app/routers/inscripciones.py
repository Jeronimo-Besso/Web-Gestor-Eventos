from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from app.database import get_db
from app.models.inscripcion import Inscripcion
from app.models.evento import Evento
from app.schemas.inscripcion import (
    InscripcionCreate,
    InscripcionResponse,
    InscripcionConEventoResponse,
)
from app.utils.dependencies import get_current_user
from app.models.usuario import Usuario
from app.models.evento import Evento

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


# Inscribirse a un evento
@router.post("/", response_model=InscripcionResponse)
def inscribirse(
    datos: InscripcionCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    # ACA FALTA SUMAR A CUPOS DE EVENTO CUANDO SEA NECESARIO
    print("Usuario:", usuario)
    print("Datos:", datos)
    evento = db.query(Evento).filter(Evento.id == datos.evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # Verificar si ya está inscrito
    ya_inscripto = (
        db.query(Inscripcion)
        .filter_by(evento_id=evento.id, usuario_id=usuario.id)
        .first()
    )
    if ya_inscripto:
        raise HTTPException(status_code=400, detail="Ya estás inscripto en este evento")

    # Verificar cupos
    inscritos = db.query(Inscripcion).filter_by(evento_id=evento.id).count()
    if inscritos >= evento.cupos:
        raise HTTPException(status_code=400, detail="No hay cupos disponibles")

    # aca debo hacer un uodate en eventos y restarle 1
    evento.inscribir()
    ####3

    inscripcion = Inscripcion(
        evento_id=evento.id, usuario_id=usuario.id, fecha_inscripcion=date.today()
    )
    # debo disminuir aca el cupo del evento
    db.add(inscripcion)
    db.commit()
    db.refresh(inscripcion)
    return InscripcionResponse(
        id=inscripcion.id,
        evento_id=inscripcion.evento_id,
        fecha_inscripcion=inscripcion.fecha_inscripcion,
    )


@router.get("/activas", response_model=List[InscripcionConEventoResponse])
def getActivas(
    db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)
):
    insc_activas = (
        db.query(Inscripcion)
        .join(Inscripcion.evento)  # asegura el join
        .filter(Inscripcion.usuario_id == usuario.id)
        .all()
    )
    return insc_activas


@router.delete("/{evento_id}")
def desinscribirse(
    evento_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    inscripcion = (
        db.query(Inscripcion)
        .filter_by(evento_id=evento_id, usuario_id=usuario.id)
        .first()
    )
    evento_obj = db.query(Evento).filter_by(id=evento_id).first()
    # esta func deberia devolver el evento que tenga ese ID
    evento_obj.desinscribir()
    # y aca deberia ejecutar desinscribir
    if not inscripcion:
        raise HTTPException(status_code=404, detail="No estás inscripto en ese evento")
    db.delete(inscripcion)
    db.commit()
    return {"detail": "Desinscripción exitosa"}
