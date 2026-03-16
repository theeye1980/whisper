import pika
import ssl
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Загружает .env из текущей директории

def get_connection():
    credentials = pika.PlainCredentials(
        os.environ.get('RABBITMQ_USER', 'admin'),
        os.environ.get('RABBITMQ_PASS', '')
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


def send_job(job_dir: str, files: list):
    conn = get_connection()
    ch = conn.channel()
    ch.queue_declare(queue='transcribe_jobs', durable=True)

    message = json.dumps({
        'job_dir': job_dir,
        'files': files
    })
    ch.basic_publish(
        exchange='',
        routing_key='transcribe_jobs',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Job sent: {job_dir}, files: {len(files)}")
    conn.close()

def declare_queue(channel, queue_name):
    channel.queue_declare(queue=queue_name, durable=True)


def publish(channel, queue_name, message):
    if isinstance(message, dict):
        message = json.dumps(message)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )