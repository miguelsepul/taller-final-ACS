# =========================================================
# Hilo escritor
# =========================================================

import threading
import time
import random


class Writer(threading.Thread):

    def __init__(self, writer_id, repository):

        super().__init__()

        self.writer_id = writer_id

        self.repository = repository

        self.name = f"Escritor-{writer_id}"

        self.writes_completed = 0

    # =====================================================
    # Método principal
    # =====================================================
    def run(self):

        for _ in range(3):

            student_id = random.randint(1, 5)

            grade = random.randint(0, 100)

            self.repository.write_grade(
                student_id,
                grade,
                self.name
            )

            self.writes_completed += 1

            time.sleep(random.uniform(0.5, 1))