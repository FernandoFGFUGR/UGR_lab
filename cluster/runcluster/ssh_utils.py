# ssh_utils.py

import paramiko
import os
import sys
from progress import update_progress_bar
import config

def execute_script_remotely(host, script_path, local_output_dir, num_outputs, total_files, extension):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sftp = None
    try:
        ssh.connect(host, username=config.REMOTE_USER, password=config.REMOTE_PASSWORD)
        sftp = ssh.open_sftp()

        remote_script_path = os.path.join("/tmp", os.path.basename(script_path))
        remote_output_dir = config.REMOTE_OUTPUT_DIR
        script_name = os.path.splitext(os.path.basename(script_path))[0]
        script_extension = os.path.splitext(script_path)[1]  # Obtiene la extensión del archivo

        # Sube y prepara el script
        sftp.put(script_path, remote_script_path)
        ssh.exec_command(f"chmod +x {remote_script_path}")
        ssh.exec_command(f"mkdir -p {remote_output_dir}")

        # Verifica la extensión y define el comando
        if script_extension == ".C":
            command = f"cd /tmp && source /opt/root/bin/thisroot.sh && root -l -b -q {os.path.basename(script_path)}"
        else:
            command = f"cd /tmp && ./{os.path.basename(script_path)}"
        
        # Ejecuta el script
        stdin, stdout, stderr = ssh.exec_command(command)

        stdout.channel.recv_exit_status()  # Espera a que el comando termine

        # Descargar los archivos output1.txt a outputN.txt
        for i in range(1, num_outputs + 1):
            remote_output_file = os.path.join(remote_output_dir, f"output{i}.{extension}")
            with config.lock:
                current_index = config.file_index
                config.file_index += 1
            local_output_file = os.path.join(
                local_output_dir,
                f"{script_name}_{current_index}.{extension}"
            )
            sftp.get(remote_output_file, local_output_file)

            # Actualizar la barra de progreso
            with config.lock:
                config.total_files_processed += 1
                update_progress_bar(config.total_files_processed, total_files)

    except Exception as e:
        with config.lock:
            print(f"\nError en {host}: {e}", file=sys.stderr)
    finally:
        if sftp:
            sftp.close()
        ssh.close()

