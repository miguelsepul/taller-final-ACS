# =========================================================
# Productor / Estudiante
# =========================================================

import threading
import random
import time

from assignment import Assignment


class StudentProducer(threading.Thread):

    def __init__(self, student_id, task_queue):

        # Inicializa Thread
        super().__init__(daemon=True)

        # ID del estudiante
        self._student_id = student_id

        # Cola compartida
        self._queue = task_queue

    # =====================================================
    # Método principal del productor
    # =====================================================
    def run(self):

        # Simular llegada aleatoria
        time.sleep(random.uniform(0, 1.5))

        # Crear tarea
        assignment = Assignment(
            student_id=self._student_id,
            course_id=f"IS{random.choice([101, 202, 303, 404])}",
            assignment_id=f"A{random.randint(1, 5)}",
            answer_text=f"Respuesta del estudiante {self._student_id}"
        )

        print(
            f"[Estudiante {self._student_id}] "
            f"Enviando tarea "
            f"{assignment.assignment_id} "
            f"del curso {assignment.course_id} "
            f"(cola: {self._queue.qsize()}/10)"
        )

        # Insertar en cola
        # Si está llena, espera automáticamente
        self._queue.put(assignment)

        print(
            f"[Estudiante {self._student_id}] "
            f"✓ Tarea encolada correctamente"
        )