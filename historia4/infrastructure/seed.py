"""
Infraestructura - Seed de datos de prueba
Crea jobs y textos simulados para demostrar los endpoints de consulta.
Como no implementamos las historias #2 y #3, simulamos los datos aquí.
"""
import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from infrastructure.job_repository import JobModel, TextResultModel


SAMPLE_TEXTS = [
    ("Me encanta este producto, es increíble", "POSITIVE", 0.92),
    ("Terrible experiencia, nunca volvería", "NEGATIVE", -0.88),
    ("El producto llegó a tiempo", "NEUTRAL", 0.05),
    ("Excelente calidad, muy recomendado", "POSITIVE", 0.95),
    ("Precio muy alto para lo que ofrece", "NEGATIVE", -0.60),
    ("El servicio al cliente fue amable", "POSITIVE", 0.70),
    ("No cumplió mis expectativas", "NEGATIVE", -0.55),
    ("Funciona como se describe", "NEUTRAL", 0.10),
    ("Fantástico, lo compraría de nuevo", "POSITIVE", 0.89),
    ("Llegó dañado, muy decepcionante", "NEGATIVE", -0.82),
    ("Calidad aceptable por el precio", "NEUTRAL", 0.15),
    ("Superó todas mis expectativas", "POSITIVE", 0.97),
    ("Instrucciones confusas e incompletas", "NEGATIVE", -0.45),
    ("Diseño bonito pero frágil", "NEUTRAL", -0.10),
    ("Lo recomendaría a mis amigos", "POSITIVE", 0.78),
]


def seed_database(db: Session, user_id: str) -> list[str]:
    """
    Crea 3 jobs de prueba para el usuario dado:
    - Job 1: completado (con todos los textos analizados)
    - Job 2: en procesamiento (parcialmente analizado)
    - Job 3: pendiente (sin analizar)

    Retorna la lista de job_ids creados.
    """
    # Verificar si ya existen jobs para este usuario
    existing = db.query(JobModel).filter(JobModel.user_id == user_id).count()
    if existing > 0:
        jobs = db.query(JobModel).filter(JobModel.user_id == user_id).all()
        return [j.id for j in jobs]

    job_ids = []

    # ── JOB 1: Completado ──────────────────────────────────────
    job1_id = str(uuid.uuid4())
    job1 = JobModel(
        id=job1_id,
        user_id=user_id,
        status="completed",
        total_texts=15,
        processed_count=15,
        created_at=datetime.utcnow() - timedelta(hours=2),
        updated_at=datetime.utcnow() - timedelta(hours=1),
    )
    db.add(job1)

    for content, sentiment, score in SAMPLE_TEXTS:
        db.add(TextResultModel(
            id=str(uuid.uuid4()),
            job_id=job1_id,
            content=content,
            sentiment=sentiment,
            score=score,
            status="completed",
            language="es",
        ))

    job_ids.append(job1_id)

    # ── JOB 2: En procesamiento ────────────────────────────────
    job2_id = str(uuid.uuid4())
    job2 = JobModel(
        id=job2_id,
        user_id=user_id,
        status="processing",
        total_texts=10,
        processed_count=4,
        created_at=datetime.utcnow() - timedelta(minutes=30),
        updated_at=datetime.utcnow() - timedelta(minutes=5),
    )
    db.add(job2)

    for i, (content, sentiment, score) in enumerate(SAMPLE_TEXTS[:10]):
        if i < 4:  # Solo los primeros 4 están analizados
            db.add(TextResultModel(
                id=str(uuid.uuid4()),
                job_id=job2_id,
                content=content,
                sentiment=sentiment,
                score=score,
                status="completed",
                language="es",
            ))
        else:
            db.add(TextResultModel(
                id=str(uuid.uuid4()),
                job_id=job2_id,
                content=content,
                sentiment=None,
                score=None,
                status="pending",
                language=None,
            ))

    job_ids.append(job2_id)

    # ── JOB 3: Pendiente ───────────────────────────────────────
    job3_id = str(uuid.uuid4())
    job3 = JobModel(
        id=job3_id,
        user_id=user_id,
        status="pending",
        total_texts=5,
        processed_count=0,
        created_at=datetime.utcnow() - timedelta(minutes=2),
        updated_at=datetime.utcnow() - timedelta(minutes=2),
    )
    db.add(job3)

    for content, _, _ in SAMPLE_TEXTS[:5]:
        db.add(TextResultModel(
            id=str(uuid.uuid4()),
            job_id=job3_id,
            content=content,
            sentiment=None,
            score=None,
            status="pending",
            language=None,
        ))

    job_ids.append(job3_id)

    db.commit()
    return job_ids
