# Proyecto Final - Arquitectura Cliente/Servidor

Repositorio correspondiente al proyecto final de la asignatura Arquitectura Cliente/Servidor.

## Integrantes
- Miguel Angel Sepúlveda Valderrama

---

# Historias implementadas

## Historia 1 - Sistema de autenticación JWT

Implementación de:
- Registro de usuarios
- Login
- JWT Authentication
- Endpoints protegidos
- Arquitectura en capas

Tecnologías:
- FastAPI
- JWT
- Pydantic

---

## Historia 4 - Consulta y reporte de Jobs

Implementación de:
- Consulta de jobs
- Reportes agregados
- Paginación
- Caché de consultas
- Seguridad JWT

Tecnologías:
- FastAPI
- Clean Architecture
- JWT

---

## Historia 8 - Concurrencia y sincronización

Implementación de:
- Productor-Consumidor
- Readers-Writers
- Barrier Synchronization

Tecnologías:
- Python Threading
- Queue
- Locks
- Condition
- Barrier

---

# Como preparar el entorno

## Crear entorno virtual

```bash
python -m venv venv
```
## Activar entorno virtual
```bash
venv\Scripts\Activate.ps1
```

## Instalar dependencias
```bash
pip install -r requirements.txt
```
o 
```bash
pip install fastapi uvicorn sqlalchemy pyjwt bcrypt "pydantic[email]" email-validator
```

# Como ejecutar los programas

## Historia 1

```bash
cd historia1
uvicorn main:app --reload
```

## Historia 4
```bash
cd historia4
uvicorn main:app --reload
```

## Historia 8
Ejecutar el programa `main.py` de cada apartado