"""
Capa de Dominio - Entidad User y Value Objects
Contiene la lógica de negocio pura, sin dependencias externas.
"""
import re
import uuid
from dataclasses import dataclass, field


# ─────────────────────────────────────────────
# VALUE OBJECTS
# Son objetos inmutables que encapsulan validación
# ─────────────────────────────────────────────

@dataclass(frozen=True)
class Email:
    """
    Value Object que garantiza que un email siempre sea válido.
    'frozen=True' lo hace inmutable: una vez creado, no cambia.
    """
    value: str

    def __post_init__(self):
        # Validación simple de formato email
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(pattern, self.value):
            raise ValueError(f"Email inválido: '{self.value}'")

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Password:
    """
    Value Object para la contraseña YA hasheada.
    El dominio solo maneja el hash, nunca el texto plano.
    """
    hashed_value: str

    def __str__(self):
        return self.hashed_value


# ─────────────────────────────────────────────
# ENTIDAD USER
# ─────────────────────────────────────────────

@dataclass
class User:
    """
    Entidad principal del dominio.
    Tiene identidad propia (id) y encapsula sus reglas de negocio.
    """
    email: Email
    password: Password
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @staticmethod
    def validate_raw_password(raw_password: str) -> None:
        """
        Regla de negocio: la contraseña debe tener al menos 8 caracteres,
        una mayúscula y un número. Se valida ANTES de hashear.
        """
        if len(raw_password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if not any(c.isupper() for c in raw_password):
            raise ValueError("La contraseña debe tener al menos una mayúscula.")
        if not any(c.isdigit() for c in raw_password):
            raise ValueError("La contraseña debe tener al menos un número.")

    @classmethod
    def create(cls, email_str: str, hashed_password: str) -> "User":
        """
        Factory Method: única forma válida de crear un User.
        Encapsula la construcción y garantiza que los Value Objects sean válidos.
        """
        email = Email(email_str)
        password = Password(hashed_password)
        return cls(email=email, password=password)
