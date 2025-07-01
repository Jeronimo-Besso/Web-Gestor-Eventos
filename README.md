# 🎟️ Sistema de Gestión de Eventos

Este proyecto consiste en una API REST desarrollada con **FastAPI** y **SQLAlchemy**, que permite gestionar eventos, inscripciones y usuarios, con autenticación basada en **JWT**. También incluye un frontend en HTML, CSS y JavaScript que consume esta API.

## 📌 Funcionalidades principales

- ✅ Registro e inicio de sesión de usuarios (con JWT).
- 🔐 Gestión de roles: usuario cliente y administrador.
- 📅 CRUD completo de eventos (admin).
- 📂 Gestión de categorías de eventos (admin).
- 📝 Inscripción a eventos (con verificación de cupos).
- 📄 Visualización de inscripciones activas.
- 🕘 Historial de inscripciones por usuario.
- 📊 Dashboard con estadísticas:
  - Total de eventos.
  - Total de inscripciones activas.
  - Promedio de inscriptos por evento.
  - Evento con más inscripciones.

---

## 🧱 Entidades del sistema

### 👤 Usuarios

- `id`: int (PK)
- `nombre`: str
- `email`: str (único)
- `contraseña`: str (encriptada)
- `rol`: str (`Administrador` o `Cliente`)

### 📅 Eventos

- `id`: int (PK)
- `nombre`, `descripcion`, `lugar`: str
- `fecha_inicio`, `fecha_fin`: date
- `cupos`: int
- `categoria_id`: int (FK)

### 📝 Inscripciones

- `id`: int (PK)
- `evento_id`: int (FK)
- `usuario_id`: int (FK)
- `fecha_inscripcion`: date

### 🗂️ Categorías

- `id`: int (PK)
- `nombre`, `descripcion`: str

---

## ⚙️ Instalación del backend

### 1. Clonar el repositorio

git clone https://github.com/Jeronimo-Besso/Pagina-Eventos.git
cd Pagina-Eventos

### 2. Crear y activar entorno virtual

python -m venv venv

source venv/bin/activate    # Linux/macOS

venv\Scripts\activate    # Windows

### 3. Instalar dependencias

pip install -r requirements.txt

### 🛠️ Configuración del entorno

El archivo .env debe estar en la raíz del proyecto. Crealo si no existe:

DATABASE_URL=mysql+mysqlconnector://usuario:contraseña@localhost:3306/nombre_de_la_base

`⚠️ Reemplazá usuario, contraseña y nombre_de_la_base con los datos reales de tu servidor MySQL.`

### 🚀 Ejecutar la aplicación

uvicorn main:app --reload

### 🌐 Frontend

El frontend utiliza HTML, CSS y JavaScript puro, y permite:

Registrarse e iniciar sesión.

Buscar y visualizar eventos disponibles.

Inscribirse a eventos (si hay cupo).

Ver las inscripciones activas.

Ver el historial de inscripciones.

`💡 Está pensado para integrarse con la API a través de fetch y JWT en headers.`

### 👥 Integrantes

- Jerónimo Besso
- Gaspar Cavallero
- Camilo Ciccioli
