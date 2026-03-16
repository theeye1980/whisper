#!/usr/bin/env python3
import os
import json
import time
import pika
import ssl
import paramiko
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS')

HOST_IP = os.environ.get('HOST_IP', '172.17.0.1')  # docker bridge
HOST_USER = os.environ.get('HOST_USER', 'vyacheslav')
HOST_KEY_PATH = '/app/ssh/id_rsa'

QUEUE_SPLIT = 'stage_split'
QUEUE_JOBS = 'transcribe_jobs'


def get_rabbit_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    ssl_context = ssl.create_default_context()
    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        ssl_options=pika.SSLOptions(ssl_context, RABBITMQ_HOST),
        heartbeat=600
    )
    return pika.BlockingConnection(params)


def run_on_host(command):
    """Запускает команду на хосте через SSH"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST_IP, username=HOST_USER, key_filename=HOST_KEY_PATH)

    stdin, stdout, stderr = ssh.exec_command(command, timeout=3600)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode()
    err = stderr.read().decode()
    ssh.close()

    return exit_code, out, err


def process_split_job(job):
    """Обработка задания на сплит"""
    job_dir = job['job_dir']
    # Путь в контейнере /app/downloads -> на хосте /home/vyacheslav/dwld
    host_dir = job_dir.replace('/app/downloads', '/home/vyacheslav/dwld')

    cmd = f'cd /home/vyacheslav/projects/whisper && python3 spliter_mass_parallel.py "{host_dir}"'
    code, out, err = run_on_host(cmd)

    if code == 0:
        return True, out
    return False, err


def process_transcribe_job(job):
    """Полный пайплайн обработки"""
    job_dir = job['job_dir']
    host_dir = job_dir.replace('/app/downloads', '/home/vyacheslav/dwld')

    scripts = [
        f'python3 spliter_mass_parallel.py "{host_dir}"',
        f'python3 wisper_local.py "{host_dir}"',
        f'python3 corr_local.py "{host_dir}"',
        f'python3 reas_mass.py "{host_dir}"',
        f'python3 ftp.py "{host_dir}"'
    ]

    for script in scripts:
        cmd = f'cd /home/vyacheslav/projects/whisper && {script}'
        code, out, err = run_on_host(cmd)
        print(f"[Host] {script}: code={code}")
        if code != 0:
            return False, f"{script}: {err}"

    return True, "OK"


def run():
    conn = get_rabbit_connection()
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE_JOBS, durable=True)
    ch.basic_qos(prefetch_count=1)

    def callback(ch, method, props, body):
        job = json.loads(body)
        print(f"[Dispatcher] Задание: {job['job_dir']}")

        ok, msg = process_transcribe_job(job)

        if ok:
            print(f"[Dispatcher] ✓ Успех")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print(f"[Dispatcher] ✗ Ошибка: {msg}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    ch.basic_consume(queue=QUEUE_JOBS, on_message_callback=callback)
    print("[Dispatcher] Слушаю очередь...")
    ch.start_consuming()


if __name__ == "__main__":
    run()