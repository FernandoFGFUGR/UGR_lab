#!/usr/bin/env python3

import paramiko
import os
import sys
sys.path.append('/usr/local/bin/runcluster')
import threading
from progress import update_progress_bar  # Importar la función de barra de progreso
import config

def copy_files_to_remote(host, user, password, local_dir, remote_dir, total_files, progress_lock, progress_counter):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sftp = None
    try:
        ssh.connect(host, username=user, password=password)
        sftp = ssh.open_sftp()

        # Recorre todos los archivos en el directorio local
        for filename in os.listdir(local_dir):
            local_path = os.path.join(local_dir, filename)
            remote_path = os.path.join(remote_dir, filename)

            if os.path.isfile(local_path):
                sftp.put(local_path, remote_path)

                # Actualizar la barra de progreso
                with progress_lock:
                    progress_counter[0] += 1
                    update_progress_bar(progress_counter[0], total_files)

    except Exception as e:
        print(f"\nError al copiar archivos a {host}: {e}")
    finally:
        if sftp:
            sftp.close()
        ssh.close()

def main():
    if len(sys.argv) != 2:
        print("Uso: ./prepare.py <directorio_local>")
        sys.exit(1)

    local_dir = sys.argv[1]

    if not os.path.isdir(local_dir):
        print(f"Error: {local_dir} no es un directorio válido")
        sys.exit(1)

    # Contar el total de archivos en el directorio
    total_files = len(os.listdir(local_dir)) * len(config.REMOTE_HOSTS)
    if total_files == 0:
        print(f"Error: no hay archivos para copiar en {local_dir}")
        sys.exit(1)

    # Variables compartidas para la barra de progreso
    progress_counter = [0]  # Lista mutable para compartir entre hilos
    progress_lock = threading.Lock()

    # Mostrar la barra de progreso inicial
    update_progress_bar(0, total_files)

    threads = []

    for host in config.REMOTE_HOSTS:
        t = threading.Thread(
            target=copy_files_to_remote,
            args=(host, config.REMOTE_USER, config.REMOTE_PASSWORD, local_dir, "/tmp", total_files, progress_lock, progress_counter)
        )
        t.start()
        threads.append(t)

    # Espera a que todos los hilos terminen
    for t in threads:
        t.join()

    print("\nCopia completada.")

if __name__ == "__main__":
    main()

