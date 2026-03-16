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
    for f in files:
        name = Path(f).stem
        chunk_dir = os.path.join(job_dir, f"temp_{name}")
        if not os.path.isdir(chunk_dir):
            return False, f"Нет папки {chunk_dir}"
        mp3s = [x for x in os.listdir(chunk_dir) if x.endswith('.mp3')]
        for mp3 in mp3s:
            txt = mp3.replace('.mp3', '.txt')
            if not os.path.exists(os.path.join(chunk_dir, txt)):
                return False, f"Нет {txt}"
    return True, "OK"

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