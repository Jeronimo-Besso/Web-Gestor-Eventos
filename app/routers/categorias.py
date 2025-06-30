from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaBase, CategoriaResponse
from app.models.evento import Evento
from app.schemas.evento import EventoResponse
from app.utils.dependencies import require_admin

router = APIRouter(prefix="/categorias", tags=["Categorías"])


# Crear una nueva categoría (solo admin)
@router.post("/", response_model=CategoriaResponse)
def crear_categoria(
    data: CategoriaBase, db: Session = Depends(get_db), _=Depends(require_admin)
):
    nueva = Categoria(nombre=data.nombre, descripcion=data.descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# Listar todas las categorías
@router.get("/getCategorias", response_model=List[CategoriaResponse])
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
