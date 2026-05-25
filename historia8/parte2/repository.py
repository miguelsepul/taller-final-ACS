# =========================================================
# Repositorio compartido con Readers-Writers Lock
# =========================================================

import time
import random
import threading

from read_write_lock import ReadWriteLock


class GradeRepository:

    def __init__(self):

        # Diccionario compartido
        self._grades = {}

        # Lock Readers-Writers
        self._lock = ReadWriteLock()

        # Estadísticas
        self.total_reads = 0
        self.total_writes = 0

        # Lock para estadísticas
        self._stats_lock = threading.Lock()

    # =====================================================
    # Obtener timestamp
    # =====================================================
    def _timestamp(self):

        return time.strftime("%H:%M:%S")

    # =====================================================
    # Lectura concurrente
    # =====================================================
    def read_grade(self, student_id, reader_name):

        self._lock.acquire_read()

        try:

            print(
                f"[{self._timestamp()}] "
                f"[{reader_name}] "
                f"Leyendo estudiante {student_id}"
            )

            # Simula lectura
            time.sleep(random.uniform(0.2, 0.6))

            grade = self._grades.get(
                student_id,
                "Sin nota"
            )

            print(
                f"[{self._timestamp()}] "
                f"[{reader_name}] "
                f"Resultado estudiante "
                f"{student_id}: {grade}"
            )

            # Actualizar estadísticas
            with self._stats_lock:
                self.total_reads += 1

            return grade

        finally:

            self._lock.release_read()

    # =====================================================
    # Escritura exclusiva
    # =====================================================
    def write_grade(
        self,
        student_id,
        grade,
        writer_name
    ):

        self._lock.acquire_write()

        try:

            print(
                f"[{self._timestamp()}] "
                f"[{writer_name}] "
                f"Actualizando estudiante "
                f"{student_id}"
            )

            # Simula escritura
            time.sleep(random.uniform(0.5, 1.2))

            self._grades[student_id] = grade

            print(
                f"[{self._timestamp()}] "
                f"[{writer_name}] "
                f"Nueva nota estudiante "
                f"{student_id}: {grade}"
            )

            # Actualizar estadísticas
            with self._stats_lock:
                self.total_writes += 1

        finally:

            self._lock.release_write()

    # =====================================================
    # Obtener notas finales
    # =====================================================
    def get_all_grades(self):

        return self._grades.copy()