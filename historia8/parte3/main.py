"""
Historia #8 - Parte 3: Barrera para inicio simultáneo de examen
═══════════════════════════════════════════════════════════════════
Simula un sistema donde:
- 5 estudiantes se conectan a la plataforma en momentos distintos
- Ninguno puede comenzar el examen hasta que TODOS estén listos
- Una vez que el último llega, todos comienzan simultáneamente
- Se usa threading.Barrier para sincronizar el inicio
"""

import threading
import time
import random


# ─────────────────────────────────────────────
# HILO - Estudiante
# ─────────────────────────────────────────────

class Student(threading.Thread):
    """
    Estudiante que se conecta y espera a sus compañeros.
    threading.Barrier garantiza que todos empiecen al mismo tiempo.
    """

    def __init__(self, student_id: int, barrier: threading.Barrier):
        super().__init__(daemon=True)
        self._id = student_id
        self._barrier = barrier
        self.exam_start_time = None

    def run(self):
        # Simula que cada estudiante llega en un momento distinto
        delay = random.uniform(0.5, 3.0)
        time.sleep(delay)

        print(f"  [Estudiante {self._id}] Se conectó a la plataforma "
              f"(tardó {delay:.1f}s en llegar). Esperando a los demás...")

        # barrier.wait() bloquea hasta que los N estudiantes lleguen.
        # Cuando el último llama a wait(), TODOS son liberados simultáneamente.
        try:
            self._barrier.wait()
        except threading.BrokenBarrierError:
            print(f"  [Estudiante {self._id}] ¡Error! La barrera fue interrumpida.")
            return

        # Este código se ejecuta al mismo tiempo para todos los estudiantes
        self.exam_start_time = time.time()
        print(f"  [Estudiante {self._id}] ¡Comenzando el examen ahora!")

        # Simula el tiempo que tarda en resolver el examen
        exam_duration = random.uniform(1.0, 3.0)
        time.sleep(exam_duration)
        print(f"  [Estudiante {self._id}] ✓ Examen entregado "
              f"(duración: {exam_duration:.1f}s)")


# ─────────────────────────────────────────────
# PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

def main():
    N = 5  # Número de estudiantes que deben estar listos antes de comenzar

    print("=" * 60)
    print("  PLATAFORMA LMS: Inicio Sincronizado de Examen")
    print("=" * 60)
    print(f"  Estudiantes requeridos para iniciar: {N}")
    print(f"  Los estudiantes llegan en momentos aleatorios (0.5s - 3.0s)")
    print(f"  El examen comienza cuando TODOS estén conectados.")
    print("=" * 60)

    # Barrier(N): se libera cuando exactamente N hilos llaman a wait()
    barrier = threading.Barrier(N)

    inicio_general = time.time()

    # Crear e iniciar los N estudiantes
    students = [Student(i + 1, barrier) for i in range(N)]
    for s in students:
        s.start()

    # Esperar a que todos terminen el examen
    for s in students:
        s.join()

    tiempo_total = time.time() - inicio_general

    # ── Estadísticas ───────────────────────────────────────────
    start_times = [s.exam_start_time for s in students if s.exam_start_time]
    if start_times:
        diferencia_inicio = max(start_times) - min(start_times)
        print("\n" + "=" * 60)
        print("  ESTADÍSTICAS FINALES")
        print("=" * 60)
        print(f"  Tiempo total del proceso:        {tiempo_total:.2f}s")
        print(f"  Diferencia entre inicios:        {diferencia_inicio*1000:.1f}ms")
        print(f"  (diferencia ~0ms demuestra que la barrera funcionó)")
        print("=" * 60)


if __name__ == "__main__":
    main()
