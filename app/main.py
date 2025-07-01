from app.database import Base, engine
from app.routers import auth, events, inscripciones, categorias, dashboard
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback

app = FastAPI(title="Sistema de Gestión de Eventos")


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            traceback.print_exc()

            return JSONResponse(
                status_code=500, content={"detail": "Ha ocurrido un error inesperado."}
            )


app.add_middleware(ErrorHandlerMiddleware)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
# Registrar routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(inscripciones.router)
app.include_router(categorias.router)
app.include_router(dashboard.router)
