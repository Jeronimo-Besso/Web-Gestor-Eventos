from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.models.evento import Evento
from app.schemas.evento import EventoResponse
from app.utils.dependencies import require_admin

router = APIRouter(prefix="/categorias", tags=["Categorías"])


# Crear una nueva categoría (solo admin)
@router.post("/", response_model=CategoriaResponse)
def crear_categoria(
    data: CategoriaCreate, db: Session = Depends(get_db), _=Depends(require_admin)
):
    nueva = Categoria(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# Listar todas las categorías
@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()


# Eliminar una categoría por ID (solo admin)
@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int, db: Session = Depends(get_db), _=Depends(require_admin)
):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()
    return {"mensaje": "Categoría eliminada correctamente"}


# Listar eventos por categoría
@router.get("/{categoria_id}/eventos", response_model=List[EventoResponse])
def eventos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    eventos = db.query(Evento).filter(Evento.categoria_id == categoria_id).all()
    if not eventos:
        raise HTTPException(
            status_code=404, detail="No se encontraron eventos para esta categoría"
        )
    return eventos
