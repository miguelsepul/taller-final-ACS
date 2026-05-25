"""
Capa de Dominio - Entidades Job y TextResult
Representan el agregado de análisis de textos.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class JobStatus(str, Enum):
    """Estados posibles de un trabajo. Regla de negocio del dominio."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Sentiment(str, Enum):
    """Etiquetas de sentimiento asignadas por el análisis."""
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"


@dataclass
class TextResult:
    """
    Entidad que representa un texto individual con su resultado de análisis.
    Pertenece al agregado Job.
    """
    content: str
    job_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sentiment: Optional[Sentiment] = None
    score: Optional[float] = None        # Valor entre -1.0 y 1.0
    status: str = "pending"              # pending | completed | failed
    language: Optional[str] = None


@dataclass
class Job:
    """
    Entidad raíz del agregado.
    Contiene la lista de textos y el estado general del trabajo.
    """
    user_id: str
    texts: List[TextResult] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    total_texts: int = 0
    processed_count: int = 0

    @classmethod
    def create(cls, user_id: str, raw_texts: List[str]) -> "Job":
        """
        Factory Method: crea un Job con sus TextResults a partir de textos crudos.
        Valida la regla de negocio: máximo 100 textos por lote.
        """
        if len(raw_texts) > 100:
            raise ValueError("El lote no puede superar 100 textos.")
        if len(raw_texts) == 0:
            raise ValueError("Debe enviar al menos un texto.")

        job = cls(user_id=user_id, total_texts=len(raw_texts))
        job.texts = [
            TextResult(content=text, job_id=job.id)
            for text in raw_texts
        ]
        return job

    @property
    def progress(self) -> str:
        """Retorna el progreso como fracción: '3/10'"""
        return f"{self.processed_count}/{self.total_texts}"
