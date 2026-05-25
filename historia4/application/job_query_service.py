"""
Capa de Aplicación - JobQueryService
Casos de uso de solo lectura: consultar estado, resultados y reportes.
Usa caché para reportes de trabajos completados (no cambian).
"""
import functools
from infrastructure.job_repository import SqlJobRepository


class JobQueryService:
    """
    Servicio de consulta de trabajos.
    Solo lectura: no modifica estado, no requiere locks de escritura.

    Caché: usa un diccionario en memoria para reportes de jobs completados.
    Una vez que un job está 'completed', su reporte es inmutable (regla de negocio),
    por lo que no tiene sentido recalcularlo en cada petición.
    """

    # Caché de clase compartida entre instancias (Singleton implícito)
    # En producción sería Redis; aquí usamos un dict en memoria.
    _report_cache: dict = {}

    def __init__(self, job_repo: SqlJobRepository):
        self._repo = job_repo

    def get_job_status(self, job_id: str, requesting_user_id: str) -> dict:
        """
        Caso de uso 1: obtener estado y progreso de un trabajo.
        Verifica que el trabajo pertenezca al usuario que lo solicita.
        """
        job = self._repo.find_by_id(job_id)

        if job is None:
            raise ValueError(f"No existe un trabajo con ID '{job_id}'.")

        if job.user_id != requesting_user_id:
            raise PermissionError("No tienes permiso para ver este trabajo.")

        return {
            "job_id": job.id,
            "status": job.status,
            "progress": f"{job.processed_count}/{job.total_texts}",
            "total_texts": job.total_texts,
            "processed_count": job.processed_count,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat(),
        }

    def get_job_results(
        self, job_id: str, requesting_user_id: str, page: int, per_page: int
    ) -> dict:
        """
        Caso de uso 2: obtener resultados detallados paginados.
        Patrón DTO: retorna solo los campos necesarios para la API.
        """
        # Validar permisos primero
        job = self._repo.find_by_id(job_id)
        if job is None:
            raise ValueError(f"No existe un trabajo con ID '{job_id}'.")
        if job.user_id != requesting_user_id:
            raise PermissionError("No tienes permiso para ver este trabajo.")

        texts, total = self._repo.find_texts_paginated(job_id, page, per_page)

        # Mapear modelos ORM a DTOs (Data Transfer Objects)
        items = [
            {
                "text_id": t.id,
                "content": t.content[:100] + "..." if len(t.content) > 100 else t.content,
                "sentiment": t.sentiment,
                "score": t.score,
                "status": t.status,
                "language": t.language,
            }
            for t in texts
        ]

        total_pages = (total + per_page - 1) // per_page  # División entera redondeada arriba

        return {
            "job_id": job_id,
            "job_status": job.status,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_items": total,
                "total_pages": total_pages,
            },
            "results": items,
        }

    def get_job_report(self, job_id: str, requesting_user_id: str) -> dict:
        """
        Caso de uso 3: obtener reporte agregado (counts + promedio).
        Usa caché: si el job está completado, el reporte no cambia nunca.
        """
        job = self._repo.find_by_id(job_id)
        if job is None:
            raise ValueError(f"No existe un trabajo con ID '{job_id}'.")
        if job.user_id != requesting_user_id:
            raise PermissionError("No tienes permiso para ver este trabajo.")

        # Solo se puede pedir reporte de trabajos completados
        if job.status != "completed":
            return {
                "job_id": job_id,
                "status": job.status,
                "message": f"El trabajo aún no está completado. Estado actual: {job.status}",
                "progress": f"{job.processed_count}/{job.total_texts}",
            }

        # Verificar caché antes de consultar la BD
        cache_key = f"report:{job_id}"
        if cache_key in self._report_cache:
            cached = self._report_cache[cache_key]
            cached["cached"] = True
            return cached

        # Calcular reporte desde la BD
        report = self._repo.get_aggregate_report(job_id)
        report["job_id"] = job_id
        report["cached"] = False

        # Guardar en caché (el reporte de un job completado es inmutable)
        self._report_cache[cache_key] = report.copy()

        return report
