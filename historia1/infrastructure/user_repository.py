"""
Capa de Infraestructura - UserRepository
Implementación concreta del contrato definido en domain/interfaces.py.
Traduce entre entidades del dominio (User) y modelos ORM (UserModel).
"""
from typing import Optional
from sqlalchemy.orm import Session

from domain.user import User
from domain.interfaces import UserRepositoryInterface
from infrastructure.database import UserModel


class SqlUserRepository(UserRepositoryInterface):
    """
    Repositorio que persiste usuarios en SQLite usando SQLAlchemy.
    Implementa la interfaz del dominio, por eso el dominio no sabe
    que existe SQLAlchemy.
    """

    def __init__(self, db: Session):
        # Recibe la sesión de BD por inyección de dependencias
        self._db = db

    def save(self, user: User) -> None:
        """Convierte la entidad de dominio a modelo ORM y la persiste."""
        db_user = UserModel(
            id=user.id,
            email=str(user.email),
            hashed_password=str(user.password),
        )
        self._db.add(db_user)
        self._db.commit()

    def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca en la BD por email.
        Convierte el modelo ORM de vuelta a entidad de dominio.
        Retorna None si no existe.
        """
        db_user = self._db.query(UserModel).filter(UserModel.email == email).first()
        if db_user is None:
            return None
        # Reconstruir la entidad de dominio desde los datos de BD
        return User.create(
            email_str=db_user.email,
            hashed_password=db_user.hashed_password,
        )

    def exists_by_email(self, email: str) -> bool:
        """Verifica existencia sin cargar el objeto completo (más eficiente)."""
        return self._db.query(
            self._db.query(UserModel).filter(UserModel.email == email).exists()
        ).scalar()
