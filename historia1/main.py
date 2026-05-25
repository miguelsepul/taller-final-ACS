"""
Punto de entrada - main.py
Inicializa FastAPI, registra las rutas y arranca el servidor.
"""
from fastapi import FastAPI
from infrastructure.database import create_tables
from presentation.routes import router

# Crear la aplicación FastAPI con metadata para Swagger
app = FastAPI(
    title="Historia #1 - Sistema de Autenticación JWT",
    description="""
## API de autenticación con Clean Architecture

### Endpoints disponibles:
- **POST /register** — Registrar nuevo usuario
- **POST /login** — Iniciar sesión y obtener token JWT
- **GET /me** — Ver perfil (requiere token)

### Cómo usar el token:
1. Regístrate con `/register`
2. Haz login con `/login` y copia el `access_token`
3. En Swagger, haz clic en el botón **Authorize 🔒** y pega el token
4. Ahora puedes acceder a `/me`
    """,
    version="1.0.0",
)

# Crear tablas al iniciar (si no existen)
create_tables()

# Registrar todas las rutas definidas en presentation/routes.py
app.include_router(router)


@app.get("/", tags=["Info"])
def root():
    """Endpoint raíz informativo."""
    return {
        "mensaje": "API de autenticación funcionando.",
        "docs": "Visita /docs para ver la documentación interactiva (Swagger UI).",
        "endpoints": ["/register", "/login", "/me"]
    }
