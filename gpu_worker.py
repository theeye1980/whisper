#!/usr/bin/env python3
"""Последовательно обрабатывает: split и whisper из очередей"""
import sys
import json
import subprocess
import filelock
sys.path.insert(0, '/home/vyacheslav/projects/whisper')

from rabbit_utils import get_connection, publish
from validators import validate_split, validate_whisper, validate_correct, validate_finalize
from config import QUEUES, WORK_DIR


LOCK_FILE = "/tmp/gpu_worker.lock"

PATH_MAP = {
    "/app/downloads": "/home/vyacheslav/dwld"
}

def docker_to_host_path(path):
    for docker_path, host_path in PATH_MAP.items():
        if path.startswith(docker_path):
            return path.replace(docker_path, host_path, 1)
    return path

def process_queue(queue_in, queue_out, scripts, validator):
    conn = get_connection()
    ch = conn.channel()
    ch.queue_declare(queue=queue_in, durable=True)
    
    method, props, body = ch.basic_get(queue=queue_in, auto_ack=False)
    if not method:
        print(f"[{queue_in}] пусто")  # <-- добавь
        conn.close()
        return False
    
    job = json.loads(body)

    job_dir_docker = job["job_dir"]
    job_dir = docker_to_host_path(job_dir_docker)
    files = job.get("files", [])
    
    print(f"[{queue_in}] {job_dir} начат")
    
    try:
        for script in scripts:  
            cmd = [sys.executable, f"{WORK_DIR}/{script}", "--input_folder", job_dir]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"{script}: {result.stderr}")
        
        ok, msg = validator(job_dir, files)
        if not ok:
            raise Exception(msg)
        
        if queue_out:
            publish(queue_out, job)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[{queue_in}] {job_dir} OK")
        conn.close()
        return True
        
    except Exception as e:
        print(f"[{queue_in}] {job_dir} ОШИБКА: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        conn.close()
        return False

def run():
    print("Запуск воркера...")
    with filelock.FileLock(LOCK_FILE):
        while True:
            print(QUEUES["input"])
            print(QUEUES["whisper"])
            # Сначала пробуем whisper (приоритет GPU-задачам)
            if process_queue(QUEUES["whisper"], QUEUES.get("correct"),
               ["wisper_local_one.py"], validate_whisper):
                continue
            
            # Потом split
            if process_queue(QUEUES["input"], None,
               ["clear_all.py", "spliter_mass_parallel.py"], validate_split):
                continue
            
            import time
            time.sleep(5)

if __name__ == "__main__":
    run()