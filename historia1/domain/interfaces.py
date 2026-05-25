"""
Capa de Dominio - Interfaces (contratos)
Define QUÉ puede hacer el repositorio, sin decir CÓMO lo hace.
Esto permite cambiar de SQLite a PostgreSQL sin tocar el dominio.
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.user import User


class UserRepositoryInterface(ABC):
    """
    Contrato abstracto para el repositorio de usuarios.
    El dominio depende de esta interfaz, NO de SQLAlchemy directamente.
    Esto es el patrón Repository: aislar el almacenamiento del dominio.
    """

    @abstractmethod
    def save(self, user: User) -> None:
        """Persiste un nuevo usuario."""
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por email. Retorna None si no existe."""
        ...

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Verifica si ya existe un usuario con ese email."""
        ...
