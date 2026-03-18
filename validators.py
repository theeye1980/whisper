import os
from pathlib import Path

def validate_split(job_dir, files):
    for f in files:
        name = Path(f).stem
        chunk_dir = os.path.join(job_dir, f"{name}")
        if not os.path.isdir(chunk_dir):
            return False, f"Нет папки {chunk_dir}"
        chunks = [x for x in os.listdir(chunk_dir) if x.endswith('.mp3')]
        if not chunks:
            return False, f"Нет чанков в {chunk_dir}"
    return True, "OK"

def validate_whisper(job_dir, files):
    """Проверяет, что создан итоговый txt файл"""
    import os
    log_file = job_dir + ".txt"
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        return True, "OK"
    return False, f"Файл {log_file} не создан или пуст"

def validate_correct(job_dir, files):
    for f in files:
        name = Path(f).stem
        chunk_dir = os.path.join(job_dir, f"temp_{name}")
        txts = [x for x in os.listdir(chunk_dir) if x.endswith('.txt')]
        for txt in txts:
            if os.path.getsize(os.path.join(chunk_dir, txt)) < 10:
                return False, f"Файл {txt} пустой"
    return True, "OK"

def validate_finalize(job_dir, files):
    for f in files:
        name = Path(f).stem
        if not os.path.exists(os.path.join(job_dir, f"{name}.txt")):
            return False, f"Нет {name}.txt"
    return True, "OK"