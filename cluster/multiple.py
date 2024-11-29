#!/usr/bin/env python3

import os
import sys
sys.path.append('/usr/local/bin/runcluster')
import threading
import queue
import time
from ssh_utils import execute_script_remotely
from progress import update_progress_bar
import config


def worker(task_queue, local_output_dir, total_files, extension):
    """Hilo trabajador para procesar tareas de la cola."""
    while not task_queue.empty():
        try:
            host, script_path = task_queue.get_nowait()
        except queue.Empty:
            break
        try:
            script_name = os.path.basename(script_path)
            execute_script_remotely(host, script_path, local_output_dir, 1, total_files, extension)
        finally:
            task_queue.task_done()


def main():
    if len(sys.argv) < 3:
        print("Uso: ./multiple.py /ruta/a/la/carpeta extension")
        sys.exit(1)

    scripts_dir = sys.argv[1]
    if not os.path.isdir(scripts_dir):
        print(f"La carpeta {scripts_dir} no existe.")
        sys.exit(1)

    extension = sys.argv[2]
    scripts = [os.path.join(scripts_dir, f) for f in os.listdir(scripts_dir) if os.path.isfile(os.path.join(scripts_dir, f))]

    if not scripts:
        print("No se encontraron scripts en la carpeta proporcionada.")
        sys.exit(1)

    print(f"Se encontraron {len(scripts)} scripts en {scripts_dir}.")

    # Calcular el total de archivos
    total_files = len(scripts)

    # Asegurarse de que la carpeta output existe
    os.makedirs(config.LOCAL_OUTPUT_DIR, exist_ok=True)
    print(f"Los resultados se guardarán en: {config.LOCAL_OUTPUT_DIR}")

    # Imprimir la barra de progreso inicial
    with config.lock:
        update_progress_bar(config.total_files_processed, total_files)

    # Crear la cola de tareas
    task_queue = queue.Queue()

    # Encolar tareas
    for script_path in scripts:
        host = config.REMOTE_HOSTS[len(task_queue.queue) % len(config.REMOTE_HOSTS)]
        task_queue.put((host, script_path))

    # Crear hilos trabajadores
    threads = []
    max_threads = min(len(config.REMOTE_HOSTS), len(scripts))  # Limitar a la cantidad de hosts disponibles
    for _ in range(max_threads):
        thread = threading.Thread(target=worker, args=(task_queue, config.LOCAL_OUTPUT_DIR, total_files, extension))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Añadir una nueva línea al finalizar la barra de progreso
    print()
    print("Todos los scripts han sido procesados.")


if __name__ == "__main__":
    main()
