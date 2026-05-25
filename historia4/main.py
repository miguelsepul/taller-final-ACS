"""
Punto de entrada - main.py
Inicializa FastAPI, registra las rutas y arranca el servidor.
"""
from fastapi import FastAPI
from infrastructure.database import create_tables
from infrastructure.job_repository import JobModel, TextResultModel  # registra los modelos
from presentation.routes import router
from presentation.job_routes import router as job_router

# Crear la aplicación FastAPI con metadata para Swagger
app = FastAPI(
    title="Historia #4 - Consulta de resultados y generación de reportes",
    description="""
## API de autenticación con Clean Architecture

### Endpoints disponibles:
- **POST /register** — Registrar nuevo usuario
- **POST /login** — Iniciar sesión y obtener token JWT
- **GET /me** — Ver perfil (requiere token)
- **POST /jobs/seed** — Crear nuevos trabajos
- **GET /jobs/{job_id}** — Estado y progreso de un trabajo específico
- **GET /jobs/{job_id}/results** — Obtener resultados paginados de un trabajo específico
- **GET /jobs/{job_id}/report** — Generar un reporte de recuento de resultados de un trabajo específico con caché

### Cómo usar el token:
1. Regístrate con `/register`
2. Haz login con `/login` y copia el `access_token`
3. En Swagger, haz clic en el botón **Authorize 🔒** y pega el token
5. Una vez autorizado, podrás crear trabajos en `/jobs/seed`
6. Consulta el estado de tus trabajos en `/jobs/{job_id}`
7. Obtén resultados paginados en `/jobs/{job_id}/results`
8. Genera reportes con `/jobs/{job_id}/report` (caché incluido para mejorar rendimiento)
    """,
    version="1.0.0",
)

# Crear tablas al iniciar (si no existen)
create_tables()

# Registrar todas las rutas definidas en presentation/routes.py
app.include_router(router)
app.include_router(job_router)


@app.get("/", tags=["Info"])
def root():
    """Endpoint raíz informativo."""
    return {
        "mensaje": "API de autenticación funcionando.",
        "docs": "Visita /docs para ver la documentación interactiva (Swagger UI).",
        "endpoints": ["/register", "/login", "/me"]
    }
