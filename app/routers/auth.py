from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.services.auth import create_access_token
from passlib.context import CryptContext
from app.schemas.usuario import UsuarioCreate


SECRET_KEY = "una_clave_secreta_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# FUNCION PARA HACER GET CUANDO EL USUARIO SE LOGUEA Y VER DONDE LO VA A REDIRIGIR LA PAGINA
@router.get("/{email}")
def checkRol(email: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="No se encuentra un usuario con ese Id"
        )
    else:
        print(user.rol)
        return {"rol": user.rol}


@router.post("/registro")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    if usuario.rol not in ("Administrador", "Cliente"):
        raise HTTPException(status_code=400, detail="Rol desconocido")
    nuevo_usuario = Usuario(
        email=usuario.email,
        hashed_password=pwd_context.hash(usuario.contraseña),
        rol=usuario.rol,
        nombre=usuario.nombre,  
    )
    db.add(nuevo_usuario)
    db.commit()
    return {"mensaje": "Usuario registrado correctamente"}
