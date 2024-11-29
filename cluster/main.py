#!/usr/bin/env python3

import os
import sys
sys.path.append('/usr/local/bin/runcluster')
import threading
import queue
import time
from ssh_utils import execute_script_remotely
from progress import update_progress_bar
from help_content import print_help
import config



def worker(task_queue, script_path, local_output_dir, num_outputs, total_files, extension):
    """Hilo trabajador para procesar tareas de la cola."""
    while not task_queue.empty():
        try:
            host, run_number = task_queue.get_nowait()
        except queue.Empty:
            break
        try:
            execute_script_remotely(host, script_path, local_output_dir, num_outputs, total_files, extension)
        finally:
            task_queue.task_done()

def main():

    if "--help" in sys.argv:
        print_help()
        sys.exit(0)

    start_time = time.time()
    if len(sys.argv) < 5:
        print("Uso: ./run.py /path/a/script.py extension ejecuciones hilos")
        sys.exit(1)

    script_path = sys.argv[1]
    if not os.path.isfile(script_path):
        print(f"El archivo {script_path} no existe.")
        sys.exit(1)

    try:
        extension = sys.argv[2]
    except ValueError:
        print("La extension no puede extar vacia.")
        sys.exit(1)

    try:
        total_runs = int(sys.argv[3])
    except ValueError:
        print("El número de ejecucioness debe ser un entero.")
        sys.exit(1)

    try:
        num_outputs = int(sys.argv[4])
    except ValueError:
        print("El número de hilos debe ser un entero.")
        sys.exit(1)


    # Calcular el total de archivos
    total_files = total_runs * num_outputs

    # Asegurarse de que la carpeta output existe
    os.makedirs(config.LOCAL_OUTPUT_DIR, exist_ok=True)
    print(f"Los resultados se guardarán en: {config.LOCAL_OUTPUT_DIR}")

    # Imprimir la barra de progreso inicial
    with config.lock:
        update_progress_bar(config.total_files_processed, total_files)

    # Crear la cola de tareas
    task_queue = queue.Queue()

    # Encolar tareas
    for i in range(total_runs):
        host = config.REMOTE_HOSTS[i % len(config.REMOTE_HOSTS)]  # Distribuye entre los hosts
        task_queue.put((host, i + 1))  # (host, número de ejecución)

    # Crear hilos trabajadores
    threads = []
    for _ in range(min(len(config.REMOTE_HOSTS), total_runs)):
        thread = threading.Thread(target=worker, args=(task_queue, script_path, config.LOCAL_OUTPUT_DIR, num_outputs, total_files, extension))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Añadir una nueva línea al finalizar la barra de progreso
    print()

    end_time = time.time()
    print(f"Tiempo total: {end_time - start_time:.2f} segundos")

if __name__ == "__main__":
    main()
