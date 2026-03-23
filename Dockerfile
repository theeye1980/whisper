FROM python:3.11-slim

WORKDIR /app

COPY mailchecker.py . 
COPY __entry1.py . 
COPY config.py . 
COPY rabbit_utils.py .
COPY .env .
COPY classes ./classes


RUN pip install --no-cache-dir requests pika python-dotenv
RUN apt-get update && apt-get install -y ffmpeg

RUN chown -R 1000:1000 /app 
CMD ["python3", "-u", "mailchecker.py"]
