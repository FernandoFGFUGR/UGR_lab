# progress.py

def update_progress_bar(total_files_processed, total_files):
    """Actualiza la barra de progreso."""
    progress = total_files_processed / total_files
    progress_bar_length = 50
    filled_length = int(progress_bar_length * progress)
    bar = '█' * filled_length + '-' * (progress_bar_length - filled_length)
    print(f'\rProgreso: |{bar}| {total_files_processed}/{total_files} archivos', end='', flush=True)
