# =========================================================
# Hilo lector
# =========================================================

import threading
import time
import random


class Reader(threading.Thread):

    def __init__(self, reader_id, repository):

        super().__init__()

        self.reader_id = reader_id

        self.repository = repository

        self.name = f"Lector-{reader_id}"

        self.reads_completed = 0

    # =====================================================
    # Método principal
    # =====================================================
    def run(self):

        for _ in range(5):

            student_id = random.randint(1, 5)

            self.repository.read_grade(
                student_id,
                self.name
            )

            self.reads_completed += 1

            time.sleep(random.uniform(0.1, 0.5))