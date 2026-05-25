"""
Capa de Infraestructura - Base de datos
Configuración de SQLAlchemy con SQLite (fácil de correr sin instalar nada extra).
En producción se cambiaría la URL a PostgreSQL sin tocar otras capas.
"""
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite guarda todo en un archivo local. No requiere servidor de BD.
DATABASE_URL = "sqlite:///./historia1.db"

engine = create_engine(
    DATABASE_URL,
    # Necesario para SQLite con múltiples hilos (thread-safe)
    connect_args={"check_same_thread": False}
)

# Fábrica de sesiones: cada petición HTTP obtiene su propia sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredan todos los modelos ORM
Base = declarative_base()


# ─────────────────────────────────────────────
# MODELO ORM (tabla en la base de datos)
# ─────────────────────────────────────────────

class UserModel(Base):
    """
    Modelo de base de datos para la tabla 'users'.
    Es independiente de la entidad User del dominio (son dos cosas distintas).
    El repositorio hace la conversión entre ambos.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


def create_tables():
    """Crea todas las tablas en la base de datos si no existen."""
    Base.metadata.create_all(bind=engine)
