"""
Capa de Aplicación - JwtService
Responsabilidad única: crear y verificar tokens JWT.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt  # PyJWT


# Clave secreta para firmar los tokens. En producción iría en variables de entorno.
SECRET_KEY = "clave_super_secreta_cambiar_en_produccion"
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24


class JwtService:
    """
    Servicio que maneja la creación y validación de tokens JWT.
    Stateless: no guarda nada en memoria ni en base de datos.
    """

    def create_token(self, user_id: str, email: str) -> str:
        """
        Crea un token JWT firmado con el ID y email del usuario.
        El token expira después de 24 horas (regla de negocio del dominio).
        """
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,          # subject: identificador del usuario
            "email": email,
            "iat": now,              # issued at: cuándo se creó
            "exp": now + timedelta(hours=TOKEN_EXPIRY_HOURS),  # expiración
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verifica y decodifica un token JWT.
        Retorna el payload si es válido, None si expiró o es inválido.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None   # Token expirado
        except jwt.InvalidTokenError:
            return None   # Token malformado o firma inválida
