"""
Historia #8 - Parte 2: Readers-Writers con prioridad a escritores
═══════════════════════════════════════════════════════════════════
Simula un sistema donde:
- 10 estudiantes (lectores) consultan sus notas concurrentemente
- 2 profesores (escritores) actualizan notas con exclusión mutua
- Los escritores tienen prioridad: si uno espera, no entran nuevos lectores
- Se generan estadísticas al final
"""

import time

from repository import GradeRepository
from reader import Reader
from writer import Writer


# =========================================================
# Configuración
# =========================================================
NUM_READERS = 10

NUM_WRITERS = 2


# =========================================================
# Encabezado
# =========================================================
print("=" * 60)

print(" SISTEMA LMS - Readers/Writers")

print("=" * 60)

print(f" Lectores concurrentes : {NUM_READERS}")

print(f" Escritores exclusivos : {NUM_WRITERS}")

print("=" * 60)


# =========================================================
# Medición de tiempo
# =========================================================
start_time = time.time()


# =========================================================
# Crear repositorio compartido
# =========================================================
repository = GradeRepository()


# =========================================================
# Crear lectores
# =========================================================
readers = [

    Reader(
        reader_id=i + 1,
        repository=repository
    )

    for i in range(NUM_READERS)
]


# =========================================================
# Crear escritores
# =========================================================
writers = [

    Writer(
        writer_id=i + 1,
        repository=repository
    )

    for i in range(NUM_WRITERS)
]


# =========================================================
# Iniciar escritores primero
# =========================================================
for writer in writers:
    writer.start()


# =========================================================
# Iniciar lectores
# =========================================================
for reader in readers:
    reader.start()


# =========================================================
# Esperar lectores
# =========================================================
for reader in readers:
    reader.join()


# =========================================================
# Esperar escritores
# =========================================================
for writer in writers:
    writer.join()


# =========================================================
# Tiempo total
# =========================================================
end_time = time.time()

total_time = end_time - start_time


# =========================================================
# Resumen final
# =========================================================
print("\n" + "=" * 60)

print(" RESUMEN FINAL")

print("=" * 60)

print(
    f" Total de lecturas realizadas : "
    f"{repository.total_reads}"
)

print(
    f" Total de escrituras realizadas : "
    f"{repository.total_writes}"
)

print(
    f" Tiempo total de ejecución : "
    f"{total_time:.2f} segundos"
)

print("\n Balanceo de carga:\n")


# Estadísticas lectores
for reader in readers:

    print(
        f" {reader.name:<15} "
        f"→ {reader.reads_completed} lecturas"
    )


print()


# Estadísticas escritores
for writer in writers:

    print(
        f" {writer.name:<15} "
        f"→ {writer.writes_completed} escrituras"
    )


print("\n Notas finales almacenadas:\n")


grades = repository.get_all_grades()

for student_id, grade in sorted(grades.items()):

    print(
        f" Estudiante {student_id}: {grade}"
    )


print("\n" + "=" * 60)