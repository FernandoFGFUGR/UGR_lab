#!/usr/bin/env python3

import paramiko
import sys
sys.path.append('/usr/local/bin/runcluster')
import threading
from progress import update_progress_bar

# Configuración de las máquinas remotas
REMOTE_HOSTS = [
    "192.168.0.201", "192.168.0.202", "192.168.0.203", "192.168.0.204",
    "192.168.0.206", "192.168.0.208", "192.168.0.209", "192.168.0.210",
    "192.168.0.211", "192.168.0.212", "192.168.0.213", "192.168.0.214",
    "192.168.0.215", "192.168.0.216"
]

REMOTE_USER = "root"

def get_password(host):
    """Generar la contraseña para el host basado en su IP."""
    last_digit = int(host.split(".")[-1])  # Convierte el último segmento a un entero
    if str(last_digit).startswith('2'):
        last_digit = int(str(last_digit)[1:])  # Quitar el primer dígito
    return f"SiPMUGR{last_digit}"

def execute_command(host, command, total_hosts, progress_lock, progress_counter):
    """Conectar al host remoto y ejecutar el comando."""
    try:
        password = get_password(host)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=REMOTE_USER, password=password)

        # Ejecutar el comando
        full_command = f"DEBIAN_FRONTEND=noninteractive bash -c \"{command}\""
        stdin, stdout, stderr = ssh.exec_command(full_command)

        # Ignorar salida estándar, pero mostrar salida de error
        error_output = stderr.read().decode().strip()
        if error_output:
            print(f"\n[Error en {host}] {error_output}")

        ssh.close()
    except Exception as e:
        print(f"\nError al conectar o ejecutar en {host}: {e}")
    finally:
        # Actualizar la barra de progreso
        with progress_lock:
            progress_counter[0] += 1
            update_progress_bar(progress_counter[0], total_hosts)


def main():
    if len(sys.argv) < 2:
        print("Uso: execute 'comando_a_ejecutar'")
        sys.exit(1)

    # Tomar el comando a ejecutar como argumento
    command = sys.argv[1]

    # Confirmar la ejecución
    print(f"Ejecutando el comando '{command}':")

    confirm = input(f"¿Estás seguro de que quieres ejecutar este comando en todos los hosts? (yes/no): ")
    if confirm.lower() != "yes":
        print("Operación cancelada.")
        return

    # Variables compartidas para la barra de progreso
    progress_counter = [0]  # Lista mutable para compartir entre hilos
    progress_lock = threading.Lock()
    total_hosts = len(REMOTE_HOSTS)

    # Mostrar la barra de progreso inicial
    update_progress_bar(progress_counter[0], total_hosts)

    # Crear y ejecutar hilos
    threads = []
    for host in REMOTE_HOSTS:
        t = threading.Thread(target=execute_command, args=(host, command, total_hosts, progress_lock, progress_counter))
        t.start()
        threads.append(t)

    # Esperar a que todos los hilos terminen
    for t in threads:
        t.join()

    print("\nEjecución completada.")

if __name__ == "__main__":
    main()
