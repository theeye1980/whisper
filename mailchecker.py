from config import imap, email_address, app_password, domain, url, chat_id, dwld_dir
import imaplib
import email
from email.header import decode_header
import time
import subprocess
import re
import requests
import mimetypes
import zipfile
import os
import shutil
from urllib.parse import unquote
from rabbit_utils import send_job

dwld_dir = os.environ.get("DWLD_DIR", "/home/vyacheslav/dwld")

IMAP_SERVER = imap
EMAIL = email_address
PASSWORD = app_password
TARGET_DOMAIN = domain
DOWNLOAD_DIR = dwld_dir


def connect():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    return mail


def decode_str(s):
    if s is None:
        return ""
    decoded, encoding = decode_header(s)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or 'utf-8', errors='ignore')
    return decoded


def download_and_extract(url_str):
    """Скачивает архив или файл и распаковывает. Возвращает абсолютный путь к папке с mp3."""
    try:
        download_url = url_str.rstrip('/') + '/download'
        print(f"Скачиваю: {download_url}")

        response = requests.get(download_url, stream=True, timeout=300)
        response.raise_for_status()

        filename = "archive.zip"
        if 'content-disposition' in response.headers:
            cd = response.headers['content-disposition']
            match = re.search(r'filename="?([^";\n]+)"?', cd)
            if match:
                filename = unquote(match.group(1))

        file_path = os.path.join(DOWNLOAD_DIR, filename)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Сохранено: {file_path}")

        # Определяем тип файла
        mime_type, _ = mimetypes.guess_type(file_path)
        is_archive = file_path.endswith(('.zip', '.tar.gz', '.tgz', '.tar', '.rar', '.7z'))

        if is_archive:
            # Распаковка архива
            extract_dir = os.path.join(DOWNLOAD_DIR, os.path.splitext(filename)[0])

            if file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as z:
                    z.extractall(extract_dir)
            elif file_path.endswith(('.tar.gz', '.tgz', '.tar')):
                import tarfile
                with tarfile.open(file_path, 'r:*') as t:
                    t.extractall(extract_dir)
            else:
                # Попытка как zip
                with zipfile.ZipFile(file_path, 'r') as z:
                    z.extractall(extract_dir)

            # Определяем финальную папку
            contents = os.listdir(extract_dir)
            if len(contents) == 1 and os.path.isdir(os.path.join(extract_dir, contents[0])):
                final_dir = os.path.join(extract_dir, contents[0])
            else:
                final_dir = extract_dir
        else:
            # Одиночный файл - создаём папку и кладём туда
            folder_name = os.path.splitext(filename)[0]
            final_dir = os.path.join(DOWNLOAD_DIR, folder_name)
            os.makedirs(final_dir, exist_ok=True)
            new_path = os.path.join(final_dir, filename)
            shutil.move(file_path, new_path)
            print(f"Одиночный файл перемещён в: {final_dir}")

        final_dir = os.path.abspath(final_dir)
        print(f"Итоговая папка: {final_dir}")

        # Отправляем задание в RabbitMQ
        mp3_in_final = [f for f in os.listdir(final_dir) if f.endswith('.mp3')]
        send_job(final_dir, mp3_in_final)

        return final_dir

    except Exception as e:
        print(f"Ошибка скачивания/распаковки: {e}")
        return None

def process_email(msg):
    subject = decode_str(msg["Subject"])
    from_ = decode_str(msg["From"])

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or 'utf-8'
                body = payload.decode(charset, errors='ignore')
                break
    else:
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset() or 'utf-8'
        body = payload.decode(charset, errors='ignore')

    print(f"От: {from_}")
    print(f"Тема: {subject}")
    print(body)

    url_dwld = extract_url(body)
    final_dir = None
    if url_dwld:
        print(f"Найдена ссылка: {url_dwld}")
        final_dir = download_and_extract(url_dwld)
    else:
        print("Ссылка не найдена")

    match = re.search(r'(Срочные:|Обычные:)', body)
    if not match:
        print("Не найдено 'Обычные:' или 'Срочные:' в письме")
        return

    content = body[match.start():]

    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(content)

    print("Записано в input.txt, запускаю __entry1.py...")

    message = f"Обработано сообщение с темой: \n {subject} \n Тело сообщения:  \n{body[:200]}...  \n Надо запустить процесс обработки и зарегистрировать рабочие файлы"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        print(f"Telegram response: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

    # Передаём final_dir через env
    env = os.environ.copy()
    if final_dir:
        env['FINAL_DIR'] = final_dir
    subprocess.run(["python3", "__entry1.py"], env=env)


def check_mail():
    mail = connect()
    mail.select("INBOX")

    status, messages = mail.search(None, f'(UNSEEN FROM "@{TARGET_DOMAIN}")')

    if status != "OK":
        mail.logout()
        return

    for num in messages[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(data[0][1])
        process_email(msg)
        mail.store(num, '+FLAGS', '\\Flagged')

    mail.logout()


def extract_url(text):
    pattern = r'https?://[^\s<>"\'\)]+[^\s<>"\'\)\.,]'
    match = re.search(pattern, text)
    return match.group(0) if match else None


if __name__ == "__main__":
    while True:
        try:
            print(f"Проверка почты...")
            check_mail()
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(10 * 60)