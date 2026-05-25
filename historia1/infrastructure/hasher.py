"""
Capa de Infraestructura - BcryptHasher
Implementación concreta del algoritmo de hashing.
Patrón Strategy: si mañana queremos usar Argon2, solo cambiamos esta clase.
"""
import bcrypt


class BcryptHasher:
    """
    Encapsula el algoritmo bcrypt para hashear y verificar contraseñas.
    bcrypt es lento por diseño: hace que los ataques de fuerza bruta sean costosos.
    """

    def hash(self, raw_password: str) -> str:
        """
        Hashea una contraseña en texto plano.
        'rounds=12' define el costo computacional (2^12 iteraciones).
        Retorna el hash como string para guardar en la BD.
        """
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        """
        Compara una contraseña en texto plano contra un hash almacenado.
        bcrypt maneja la extracción del salt internamente.
        Retorna True si coinciden, False si no.
        """
        return bcrypt.checkpw(
            raw_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
