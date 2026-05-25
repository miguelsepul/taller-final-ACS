"""
Capa de Aplicación - AuthService
Orquesta los casos de uso: registrar usuario y autenticar usuario.
Depende de interfaces (no de implementaciones concretas).
"""
import threading
from domain.user import User
from domain.interfaces import UserRepositoryInterface
from application.jwt_service import JwtService


class AuthService:
    """
    Servicio de aplicación que implementa los casos de uso de autenticación.

    Thread-safe: usa RLock para proteger operaciones críticas donde
    múltiples solicitudes de login/registro podrían llegar simultáneamente.
    RLock (Reentrant Lock) permite que el mismo hilo lo adquiera varias veces
    sin bloquearse a sí mismo.
    """

    def __init__(self, user_repo: UserRepositoryInterface, hasher, jwt_service: JwtService):
        self._user_repo = user_repo
        self._hasher = hasher
        self._jwt = jwt_service
        self._lock = threading.RLock()  # Protege secciones críticas

    # ─────────────────────────────────────────────
    # CASO DE USO 1: Registro de nuevo usuario
    # ─────────────────────────────────────────────
    def register(self, email: str, raw_password: str) -> str:
        """
        Registra un nuevo usuario en el sistema.
        Retorna el ID del usuario creado.
        Lanza ValueError si el email ya existe o la contraseña no cumple reglas.
        """
        # Validar contraseña ANTES de cualquier operación costosa
        # (esta validación está en el dominio, regla de negocio pura)
        User.validate_raw_password(raw_password)

        # RLock protege la sección crítica: verificar existencia + guardar
        # Sin esto, dos registros simultáneos con el mismo email podrían
        # pasar la verificación y causar duplicados (race condition).
        with self._lock:
            if self._user_repo.exists_by_email(email):
                raise ValueError(f"Ya existe un usuario con el email '{email}'.")

            # Hashear contraseña (nunca se guarda en texto plano)
            hashed = self._hasher.hash(raw_password)

            # Factory Method del dominio crea el User con Value Objects validados
            user = User.create(email_str=email, hashed_password=hashed)

            self._user_repo.save(user)

        return user.id

    # ─────────────────────────────────────────────
    # CASO DE USO 2: Autenticación (login)
    # ─────────────────────────────────────────────
    def login(self, email: str, raw_password: str) -> str:
        """
        Autentica un usuario y retorna un token JWT.
        Lanza ValueError si las credenciales son incorrectas.

        Nota de seguridad: siempre decimos "credenciales inválidas" sin
        especificar si el email o la contraseña fue lo incorrecto.
        Esto evita que un atacante descubra qué emails están registrados.
        """
        # Login es lectura + comparación, no modifica estado compartido,
        # pero el lock protege si hubiera caché interna en el futuro.
        with self._lock:
            user = self._user_repo.find_by_email(email)

        if user is None:
            raise ValueError("Credenciales inválidas.")

        # Verificar contraseña contra el hash almacenado
        password_ok = self._hasher.verify(raw_password, str(user.password))
        if not password_ok:
            raise ValueError("Credenciales inválidas.")

        # Crear y retornar token JWT (expira en 24h)
        token = self._jwt.create_token(user_id=user.id, email=str(user.email))
        return token

    # ─────────────────────────────────────────────
    # CASO DE USO 3: Verificar token (usado en middleware)
    # ─────────────────────────────────────────────
    def verify_token(self, token: str) -> dict:
        """
        Verifica un token JWT y retorna su payload.
        Lanza ValueError si el token es inválido o expiró.
        """
        payload = self._jwt.verify_token(token)
        if payload is None:
            raise ValueError("Token inválido o expirado.")
        return payload
