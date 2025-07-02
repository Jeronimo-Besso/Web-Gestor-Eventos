from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoResponse
from app.utils.dependencies import get_current_user, require_admin
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.models.categoria import Categoria

router = APIRouter(prefix="/eventos", tags=["Eventos"])


# Obtener todos los eventos disponibles
@router.get("/", response_model=List[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return (
        db.query(Evento)
        .options(joinedload(Evento.categoria))
        .filter(Evento.categoria_id != None)
        .all()
    )


# Buscar eventos por nombre o descripción
@router.get("/buscar", response_model=List[EventoResponse])
def buscar_eventos(q: str, db: Session = Depends(get_db)):
    resultados = (
        db.query(Evento)
        .join(Evento.categoria)  # join a la tabla Categoria
        .options(joinedload(Evento.categoria))  # eager load para respuesta
        .filter(
            or_(
                Evento.nombre.ilike(f"%{q}%"),
                Categoria.nombre.ilike(f"%{q}%"),  # filtra por nombre de la categoría
            )
        )
        .all()
    )
    return resultados


# Crear un nuevo evento (solo admin)
@router.post("/", response_model=EventoResponse)
def crear_evento(
    evento: EventoCreate, db: Session = Depends(get_db), usuario=Depends(require_admin)
):
    nuevo_evento = Evento(**evento.dict())
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)

    db.refresh(nuevo_evento)
    _ = nuevo_evento.categoria

    return nuevo_evento


# Editar un evento existente (solo admin)
@router.put("/{evento_id}", response_model=EventoResponse)
def actualizar_evento(
    evento_id: int,
    datos: EventoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_admin),
):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    for clave, valor in datos.dict().items():
        setattr(evento, clave, valor)
    db.commit()
    db.refresh(evento)
    return evento


# Eliminar un evento (solo admin)
@router.delete("/{evento_id}")
def eliminar_evento(
    evento_id: int, db: Session = Depends(get_db), usuario=Depends(require_admin)
):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    db.delete(evento)
    db.commit()
    return {"mensaje": "Evento eliminado exitosamente"}


@router.get("/{evento_id}", response_model=EventoResponse)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento
