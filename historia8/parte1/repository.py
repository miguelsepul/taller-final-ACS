# =========================================================
# Repositorio thread-safe de notas
# =========================================================

import threading


class GradeRepository:

    def __init__(self):

        # Diccionario compartido:
        # {student_id: [grades]}
        self._grades = {}

        # RLock:
        # Permite múltiples adquisiciones del mismo hilo
        self._lock = threading.RLock()

    # =====================================================
    # Guardar nota
    # =====================================================
    def save_grade(self, student_id, grade):

        with self._lock:

            # Si el estudiante no existe, crear lista
            if student_id not in self._grades:
                self._grades[student_id] = []

            # Agregar nota
            self._grades[student_id].append(grade)

    # =====================================================
    # Obtener notas de un estudiante
    # =====================================================
    def get_grades(self, student_id):

        with self._lock:

            return self._grades.get(student_id, []).copy()

    # =====================================================
    # Obtener todas las notas
    # =====================================================
    def get_all_grades(self):

        with self._lock:

            return {
                sid: grades.copy()
                for sid, grades in self._grades.items()
            }