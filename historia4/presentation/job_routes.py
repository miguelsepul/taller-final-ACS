"""
Capa de Presentación - Endpoints de Jobs (Historia #4)
Endpoints para consultar estado, resultados y reportes de trabajos.
Todos los endpoints están protegidos con JWT.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from infrastructure.database import SessionLocal
from infrastructure.job_repository import SqlJobRepository
from infrastructure.seed import seed_database
from application.job_query_service import JobQueryService
from presentation.routes import get_current_user


# ─────────────────────────────────────────────
# DEPENDENCIAS
# ─────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_job_query_service(db: Session = Depends(get_db)) -> JobQueryService:
    repo = SqlJobRepository(db)
    return JobQueryService(job_repo=repo)


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────

router = APIRouter(prefix="/jobs", tags=["Consulta de Jobs"])


@router.post(
    "/seed",
    summary="Crear datos de prueba",
    description="Crea 3 jobs de prueba (completado, en proceso, pendiente) para el usuario autenticado.",
)
def create_seed_data(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Endpoint especial para poblar la BD con datos de prueba.
    En un sistema real no existiría; aquí simula las historias #2 y #3.
    """
    user_id = current_user["sub"]
    job_ids = seed_database(db, user_id)
    return {
        "message": "Datos de prueba creados exitosamente.",
        "job_ids": job_ids,
        "tip": "Usa estos IDs para probar los endpoints de consulta.",
    }


@router.get(
    "/{job_id}",
    summary="Estado y progreso de un trabajo",
    description="Retorna el estado actual del trabajo y cuántos textos han sido procesados.",
)
def get_job_status(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    service: JobQueryService = Depends(get_job_query_service),
):
    """
    Caso de uso 1: consultar estado y progreso.
    Criterio de aceptación: retorna estado y progreso del job.
    """
    try:
        return service.get_job_status(job_id, requesting_user_id=current_user["sub"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get(
    "/{job_id}/results",
    summary="Resultados paginados de un trabajo",
    description="Retorna la lista paginada de textos con su análisis de sentimiento.",
)
def get_job_results(
    job_id: str,
    page: int = Query(default=1, ge=1, description="Número de página"),
    per_page: int = Query(default=5, ge=1, le=50, description="Resultados por página"),
    current_user: dict = Depends(get_current_user),
    service: JobQueryService = Depends(get_job_query_service),
):
    """
    Caso de uso 2: resultados detallados con paginación.
    Criterio: GET /jobs/{job_id}/results?page=1&per_page=5
    """
    try:
        return service.get_job_results(
            job_id,
            requesting_user_id=current_user["sub"],
            page=page,
            per_page=per_page,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get(
    "/{job_id}/report",
    summary="Reporte agregado de un trabajo",
    description="Retorna conteos de sentimientos y score promedio. Solo disponible para jobs completados.",
)
def get_job_report(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    service: JobQueryService = Depends(get_job_query_service),
):
    """
    Caso de uso 3: reporte agregado con caché.
    Criterio: retorna {positive_count, negative_count, neutral_count, average_score}
    """
    try:
        return service.get_job_report(
            job_id,
            requesting_user_id=current_user["sub"],
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
