"""
Historia #8 - Parte 1: Plataforma LMS - Productor/Consumidor
═══════════════════════════════════════════════════════════════
Simula un sistema donde:
- 15 estudiantes (productores/hilos) envían tareas a una cola
- 3 profesores virtuales (workers/consumidores) las corrigen concurrentemente
- La cola tiene capacidad máxima de 10 tareas
- El GradeRepository es thread-safe con RLock
"""

import queue
import threading

from repository import GradeRepository
from worker import AssignmentWorker
from producer import StudentProducer


# =========================================================
# Configuración del sistema
# =========================================================
NUM_STUDENTS = 15

NUM_WORKERS = 3

QUEUE_SIZE = 10


# =========================================================
# Encabezado
# =========================================================
print("=" * 60)

print("  PLATAFORMA LMS - Productor/Consumidor")

print("=" * 60)

print(f"  Estudiantes productores: {NUM_STUDENTS}")

print(f"  Profesores virtuales: {NUM_WORKERS}")

print(f"  Capacidad máxima de cola: {QUEUE_SIZE}")

print("=" * 60)


# =========================================================
# Cola compartida thread-safe
# =========================================================
task_queue = queue.Queue(maxsize=QUEUE_SIZE)


# =========================================================
# Repositorio compartido
# =========================================================
grade_repository = GradeRepository()


# =========================================================
# Evento de apagado limpio
# =========================================================
stop_event = threading.Event()


# =========================================================
# Crear workers
# =========================================================
workers = [

    AssignmentWorker(
        name=f"Profesor-{chr(65 + i)}",
        task_queue=task_queue,
        grade_repository=grade_repository,
        stop_event=stop_event
    )

    for i in range(NUM_WORKERS)
]


# =========================================================
# Iniciar workers
# =========================================================
for worker in workers:
    worker.start()


# =========================================================
# Crear productores
# =========================================================
students = [

    StudentProducer(
        student_id=i + 1,
        task_queue=task_queue
    )

    for i in range(NUM_STUDENTS)
]


# =========================================================
# Iniciar productores
# =========================================================
for student in students:
    student.start()


# =========================================================
# Esperar estudiantes
# =========================================================
for student in students:
    student.join()


print("\n[SISTEMA] Todos los estudiantes enviaron tareas")


# =========================================================
# Esperar procesamiento total
# =========================================================
task_queue.join()


print("[SISTEMA] Todas las tareas fueron corregidas")


# =========================================================
# Detener workers
# =========================================================
stop_event.set()


# =========================================================
# Esperar cierre de workers
# =========================================================
for worker in workers:
    worker.join()


# =========================================================
# Resumen final
# =========================================================
print("\n" + "=" * 60)

print("  RESUMEN FINAL DE NOTAS")

print("=" * 60)


all_grades = grade_repository.get_all_grades()


for student_id in sorted(all_grades.keys()):

    grades = all_grades[student_id]

    average = sum(grades) / len(grades)

    print(
        f"  Estudiante {student_id:2d}: "
        f"{grades[0]:.1f} "
        f"(promedio: {average:.1f})"
    )


print(
    f"\n  Total de estudiantes evaluados: "
    f"{len(all_grades)}"
)

print("=" * 60)