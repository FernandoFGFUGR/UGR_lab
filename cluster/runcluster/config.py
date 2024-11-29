# config.py

import os
import threading

# Configuración de las máquinas remotas
REMOTE_HOSTS = [
    "192.168.0.201", "192.168.0.202", "192.168.0.203", "192.168.0.204",
    "192.168.0.206", "192.168.0.208", "192.168.0.209", "192.168.0.210",
    "192.168.0.211", "192.168.0.212", "192.168.0.213", "192.168.0.214",
    "192.168.0.215", "192.168.0.216"
]

REMOTE_USER = "usuario"
REMOTE_PASSWORD = "usuario"
REMOTE_OUTPUT_DIR = "/tmp/output"

# Determinar el directorio de salida dinámico basado en el usuario
LOCAL_OUTPUT_DIR = os.path.join(os.getenv("HOME"), "output")

# Variables compartidas y Lock
total_files_processed = 0
lock = threading.Lock()
file_index = 0
