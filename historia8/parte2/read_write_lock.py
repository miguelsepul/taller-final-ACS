# =========================================================
# ReadWriteLock con prioridad a escritores
# =========================================================

import threading


class ReadWriteLock:

    def __init__(self):

        # Condition permite:
        # - esperar
        # - despertar hilos
        # - coordinar concurrencia
        self.condition = threading.Condition()

        # Número actual de lectores activos
        self.readers = 0

        # Indica si un escritor está escribiendo
        self.writer_active = False

        # Número de escritores esperando
        self.writers_waiting = 0

    # =====================================================
    # Adquirir permiso de lectura
    # =====================================================
    def acquire_read(self):

        with self.condition:

            # Si hay escritor activo
            # o escritores esperando,
            # el lector debe esperar
            while (
                self.writer_active
                or self.writers_waiting > 0
            ):
                self.condition.wait()

            # Nuevo lector entra
            self.readers += 1

    # =====================================================
    # Liberar lectura
    # =====================================================
    def release_read(self):

        with self.condition:

            # Lector termina
            self.readers -= 1

            # Si ya no quedan lectores,
            # despertar escritores
            if self.readers == 0:
                self.condition.notify_all()

    # =====================================================
    # Adquirir permiso de escritura
    # =====================================================
    def acquire_write(self):

        with self.condition:

            # Nuevo escritor esperando
            self.writers_waiting += 1

            # Esperar mientras:
            # - haya lectores
            # - otro escritor esté activo
            while (
                self.readers > 0
                or self.writer_active
            ):
                self.condition.wait()

            # Este escritor ya no espera
            self.writers_waiting -= 1

            # Escritura exclusiva activa
            self.writer_active = True

    # =====================================================
    # Liberar escritura
    # =====================================================
    def release_write(self):

        with self.condition:

            # Escritura terminada
            self.writer_active = False

            # Despertar todos los hilos esperando
            self.condition.notify_all()