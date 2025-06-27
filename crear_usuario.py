from passlib.context import CryptContext
from app.models.usuario import Usuario
from app.database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

nuevo_usuario = Usuario(
    nombre="Administrador",
    email="administrador@hotmail.com",
    hashed_password=pwd_context.hash("1234"),
    rol="Administrador",
)

db.add(nuevo_usuario)
db.commit()
db.close()
