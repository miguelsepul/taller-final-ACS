# =========================================================
# Worker / Profesor virtual
# Consumidor de tareas
# =========================================================

import threading
import random
import time
import queue


class AssignmentWorker(threading.Thread):

    def __init__(
        self,
        name,
        task_queue,
        grade_repository,
        stop_event
    ):

        # Inicializa Thread
        super().__init__(name=name, daemon=True)

        # Cola compartida
        self._queue = task_queue

        # Repositorio compartido
        self._repository = grade_repository

        # Evento para cierre ordenado
        self._stop_event = stop_event

        # Estadística de tareas procesadas
        self._tasks_processed = 0

    # =====================================================
    # Método principal del worker
    # =====================================================
    def run(self):

        # Ejecuta mientras el sistema siga activo
        while not self._stop_event.is_set():

            try:

                # Obtener tarea de la cola
                # timeout evita bloqueo infinito
                assignment = self._queue.get(timeout=0.5)

            except queue.Empty:

                # Si la cola está vacía, volver a intentar
                continue

            # Procesar tarea
            self._correct_assignment(assignment)

            # Marcar tarea completada
            self._queue.task_done()

            # Incrementar contador
            self._tasks_processed += 1

        print(
            f"  [{self.name}] Finalizando. "
            f"Tareas corregidas: {self._tasks_processed}"
        )

    # =====================================================
    # Simular corrección
    # =====================================================
    def _correct_assignment(self, assignment):

        # Tiempo aleatorio de corrección
        correction_time = random.uniform(0.5, 2.0)

        print(
            f"  [{self.name}] Corrigiendo tarea "
            f"de Estudiante {assignment.student_id} "
            f"(curso: {assignment.course_id}, "
            f"tarea: {assignment.assignment_id})..."
        )

        # Simulación de trabajo
        time.sleep(correction_time)

        # Generar nota aleatoria
        grade = random.uniform(0, 100)

        # Guardar nota
        self._repository.save_grade(
            assignment.student_id,
            grade
        )

        print(
            f"  [{self.name}] ✓ "
            f"Estudiante {assignment.student_id} "
            f"→ Nota: {grade:.1f} "
            f"(en {correction_time:.1f}s)"
        )