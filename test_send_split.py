#!/usr/bin/env python3
"""
Тестовый скрипт для заполнения очереди stage_split в RabbitMQ.
Использует тот же rabbit_utils.py, но отправляет в другую очередь.
"""

import pika
import ssl
import os
import json
from config import RABBITMQ_PASS

def get_connection():
    credentials = pika.PlainCredentials(
        os.environ.get('RABBITMQ_USER', 'admin'),
        RABBITMQ_PASS
    )
    ssl_context = ssl.create_default_context()
    host = os.environ.get('RABBITMQ_HOST', 'rabbitmq.theyen8n.ru')
    ssl_options = pika.SSLOptions(ssl_context, host)

    params = pika.ConnectionParameters(
        host=host,
        port=int(os.environ.get('RABBITMQ_PORT', 5672)),
        virtual_host='/',
        credentials=credentials,
        ssl_options=ssl_options,
        heartbeat=600,
        blocked_connection_timeout=300,
    )
    return pika.BlockingConnection(params)


def send_to_stage_split(job_dir: str, files: list):
    conn = get_connection()
    ch = conn.channel()
    ch.queue_declare(queue='stage_split', durable=True)

    message = json.dumps({
        'job_dir': job_dir,
        'files': files
    })
    ch.basic_publish(
        exchange='',
        routing_key='stage_split',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Job sent to stage_split: {job_dir}, files: {files}")
    conn.close()


if __name__ == "__main__":
    # Тестовые данные на основе твоей структуры
    job_dir = "/home/vyacheslav/dwld/03.12_3_zom1_12.30_(02.23)"
    files = ["03.05_2_zs_11.00_(00.51).mp3"]

    send_to_stage_split(job_dir, files)