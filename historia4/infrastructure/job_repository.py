"""
Capa de Infraestructura - Modelos ORM y repositorio de Jobs
Extiende la base de datos con las tablas jobs y text_results.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Session, relationship

from infrastructure.database import Base
from domain.job import Job, JobStatus, TextResult, Sentiment


# ─────────────────────────────────────────────
# MODELOS ORM
# ─────────────────────────────────────────────

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    status = Column(String, default="pending", nullable=False)
    total_texts = Column(Integer, default=0)
    processed_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relación uno-a-muchos con TextResultModel
    texts = relationship("TextResultModel", back_populates="job", lazy="dynamic")


class TextResultModel(Base):
    __tablename__ = "text_results"

    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.id"), index=True, nullable=False)
    content = Column(String, nullable=False)
    sentiment = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    status = Column(String, default="pending")
    language = Column(String, nullable=True)

    job = relationship("JobModel", back_populates="texts")


# ─────────────────────────────────────────────
# REPOSITORIO
# ─────────────────────────────────────────────

class SqlJobRepository:
    """
    Repositorio que maneja la persistencia de Jobs y TextResults.
    Implementa el patrón Repository: aísla SQLAlchemy del dominio.
    """

    def __init__(self, db: Session):
        self._db = db

    def save(self, job: Job) -> None:
        """Persiste un Job completo con todos sus textos."""
        db_job = JobModel(
            id=job.id,
            user_id=job.user_id,
            status=job.status.value,
            total_texts=job.total_texts,
            processed_count=job.processed_count,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        self._db.add(db_job)

        for text in job.texts:
            db_text = TextResultModel(
                id=text.id,
                job_id=text.job_id,
                content=text.content,
                sentiment=text.sentiment.value if text.sentiment else None,
                score=text.score,
                status=text.status,
                language=text.language,
            )
            self._db.add(db_text)

        self._db.commit()

    def find_by_id(self, job_id: str) -> Optional[JobModel]:
        """Busca un job por ID. Retorna el modelo ORM directamente."""
        return self._db.query(JobModel).filter(JobModel.id == job_id).first()

    def find_texts_paginated(
        self, job_id: str, page: int, per_page: int
    ) -> tuple[List[TextResultModel], int]:
        """
        Retorna textos paginados de un job junto con el total.
        Patrón Query Object: encapsula lógica de paginación.
        """
        query = self._db.query(TextResultModel).filter(
            TextResultModel.job_id == job_id
        )
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        return items, total

    def get_aggregate_report(self, job_id: str) -> dict:
        """
        Calcula el reporte agregado directamente en la BD (más eficiente).
        Retorna conteos por sentimiento y score promedio.
        """
        texts = self._db.query(TextResultModel).filter(
            TextResultModel.job_id == job_id,
            TextResultModel.status == "completed"
        ).all()

        positive = sum(1 for t in texts if t.sentiment == "POSITIVE")
        negative = sum(1 for t in texts if t.sentiment == "NEGATIVE")
        neutral = sum(1 for t in texts if t.sentiment == "NEUTRAL")
        scores = [t.score for t in texts if t.score is not None]
        avg_score = round(sum(scores) / len(scores), 4) if scores else 0.0

        return {
            "positive_count": positive,
            "negative_count": negative,
            "neutral_count": neutral,
            "average_score": avg_score,
            "total_analyzed": len(texts),
        }
