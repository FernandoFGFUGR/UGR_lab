# help_content.py

def print_help():
    help_text = """
Uso: ./run.py /path/a/script.py extension ejecuciones hilos

Argumentos:
    /path/a/script.py  Ruta al script que se ejecutará.
    extension          Extensión de los archivos de salida (por ejemplo: txt, csv, root).
    CPUs               Número de ejecuciones totales del script.
    hilos              Número de hilos paralelos que se usarán.

Opciones:
    --help             Muestra esta ayuda y termina la ejecución.
    
Ejemplo:
    ./run.py /path/a/script.py txt 4 8
"""
    print(help_text)
