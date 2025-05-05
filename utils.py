import os
import time

def cleanup_old_files(folder_path, days=15):
    """
    Delete files older than `days` in the given folder.
    """
    now = time.time()
    cutoff = now - (days * 86400)

    if not os.path.exists(folder_path):
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and os.path.getmtime(file_path) < cutoff:
            try:
                os.remove(file_path)
            except Exception:
                pass
