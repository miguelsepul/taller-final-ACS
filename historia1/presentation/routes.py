"""
Capa de Presentación - Endpoints FastAPI
Define las rutas HTTP y los DTOs (esquemas de entrada/salida).
No contiene lógica de negocio: delega todo al AuthService.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from infrastructure.database import SessionLocal
from infrastructure.user_repository import SqlUserRepository
from infrastructure.hasher import BcryptHasher
from application.auth_service import AuthService
from application.jwt_service import JwtService


# ─────────────────────────────────────────────
# DTOs (Data Transfer Objects) con Pydantic
# Definen la forma exacta del JSON de entrada y salida
# ─────────────────────────────────────────────

class RegisterRequest(BaseModel):
    """JSON esperado en POST /register"""
    email: EmailStr          # Pydantic valida el formato de email automáticamente
    password: str


class RegisterResponse(BaseModel):
    """JSON retornado tras registro exitoso"""
    user_id: str
    message: str


class LoginRequest(BaseModel):
    """JSON esperado en POST /login"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """JSON retornado tras login exitoso"""
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    """JSON retornado en GET /me (endpoint protegido de ejemplo)"""
    user_id: str
    email: str
    message: str


# ─────────────────────────────────────────────
# DEPENDENCIAS (Inyección de Dependencias de FastAPI)
# FastAPI las llama automáticamente en cada petición
# ─────────────────────────────────────────────

def get_db():
    """
    Proporciona una sesión de BD por petición.
    El bloque finally garantiza que siempre se cierre, incluso si hay error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """
    Construye el AuthService con todas sus dependencias.
    Esto es Inyección de Dependencias manual: el controlador no sabe
    cómo se construyen los servicios, solo los recibe listos.
    """
    repo = SqlUserRepository(db)
    hasher = BcryptHasher()
    jwt_svc = JwtService()
    return AuthService(user_repo=repo, hasher=hasher, jwt_service=jwt_svc)


# Esquema de seguridad Bearer Token para Swagger UI
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Middleware de autenticación: se usa como dependencia en endpoints protegidos.
    Extrae el token del header 'Authorization: Bearer <token>' y lo verifica.
    Si el token es inválido, FastAPI retorna automáticamente 401.
    """
    token = credentials.credentials
    try:
        payload = auth_service.verify_token(token)
        return payload
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ─────────────────────────────────────────────
# ROUTER Y ENDPOINTS
# ─────────────────────────────────────────────

router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    tags=["Autenticación"],
)
def register(request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)):
    """
    Registra un nuevo usuario en el sistema.
    - El email debe ser único.
    - La contraseña debe tener mínimo 8 caracteres, una mayúscula y un número.
    """
    try:
        user_id = auth_service.register(
            email=request.email,
            raw_password=request.password,
        )
        return RegisterResponse(
            user_id=user_id,
            message="Usuario registrado exitosamente."
        )
    except ValueError as e:
        # Error de negocio (email duplicado, contraseña débil) → 400 Bad Request
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    tags=["Autenticación"],
)
def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    """
    Autentica un usuario y retorna un token JWT válido por 24 horas.
    Usa el token en el header: `Authorization: Bearer <token>`
    """
    try:
        token = auth_service.login(
            email=request.email,
            raw_password=request.password,
        )
        return LoginResponse(access_token=token)
    except ValueError as e:
        # Credenciales incorrectas → 401 Unauthorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get(
    "/me",
    response_model=MeResponse,
    summary="Ver mi perfil (endpoint protegido)",
    tags=["Protegido"],
)
def get_me(current_user: dict = Depends(get_current_user)):
    """
    Endpoint protegido de ejemplo.
    Solo accesible con un token JWT válido en el header Authorization.
    Demuestra que el middleware de autenticación funciona.
    """
    return MeResponse(
        user_id=current_user["sub"],
        email=current_user["email"],
        message="Token válido. Acceso concedido."
    )
