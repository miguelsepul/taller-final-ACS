# =========================================================
# DTO - Tarea del estudiante
# =========================================================

from dataclasses import dataclass


@dataclass
class Assignment:

    # ID del estudiante
    student_id: int

    # ID del curso
    course_id: str

    # ID de la tarea
    assignment_id: str

    # Respuesta enviada
    answer_text: str