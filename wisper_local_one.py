import os
import sys
import argparse
import torch
import time
from ftplib import FTP
sys.path.insert(0, '/home/vyacheslav/projects/whisper')

from faster_whisper import WhisperModel
from classes.Whisperlocal import Whisperlocal
from classes.TextFileReader import TextFileReader
from config import input_folder, parts_time, initial_time, segments,ftp_path,ftp_host,ftp_user_name, ftp_password,SMTP_HOST,SMTP_PORT,EMAIL_ADDRESS,APP_PASSWORD

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header



parser = argparse.ArgumentParser(description='Обработка аудио файлов')
parser.add_argument('--input_folder', type=str, default=None, help='Путь к папке с аудио файлами')
args = parser.parse_args()

print(f"CUDA доступен: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Текущее устройство: {torch.cuda.current_device()}")
    print(f"Имя устройства: {torch.cuda.get_device_name(torch.cuda.current_device())}")

whisper_model = WhisperModel("large-v3", device="cuda", compute_type="float16")

def process_file(file_name, start_time, output_folder, whisper_net, language='ru'):
    try:
        chunk_start = time.time()
        segments_result, info = whisper_model.transcribe(
            os.path.join(output_folder, file_name),
            language=language,
            beam_size=1,
            condition_on_previous_text=False,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        segments_list = list(segments_result)
        chunk_time = time.time() - chunk_start
        whisper_net.segments_text(start_time, segments, segments_list)
        print(f"Обработано за {chunk_time:.2f} сек")
    except Exception as e:
        print(f"Ошибка обработки {file_name}: {e}")
        raise
# Отправка письма
def send_email(filename):
    smtp_host = SMTP_HOST
    smtp_port = SMTP_PORT
    email_address = EMAIL_ADDRESS
    app_password = APP_PASSWORD
    
    subject = f"{filename} обработан"
    link = f"https://podvi.ru/n8n/{filename}"
    
    # HTML-тело с ссылкой
    html_body = f'''
    <html>
    <body>
        <p>Файл обработан:</p>
        <p><a href="{link}">{link}</a></p>
    </body>
    </html>
    '''
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = email_address
    msg['To'] = "v.kosarev@list.ru"
    msg['Cc'] = "kattyrinoa@mail.ru"
    
    # Текстовая и HTML версии
    text_part = MIMEText(link, 'plain', 'utf-8')
    html_part = MIMEText(html_body, 'html', 'utf-8')
    msg.attach(text_part)
    msg.attach(html_part)
    
    recipients = ["v.kosarev@list.ru", "kattyrinoa@mail.ru"]
    #recipients = ["v.kosarev@list.ru"]
    
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(email_address, app_password)
        server.sendmail(email_address, recipients, msg.as_string())
    
    print(f"Email отправлен: {subject}")

def main(folder):
    output_folder = folder
    log_file = output_folder + ".txt"

    txt = TextFileReader("")
    file_list = txt.sort_files_in_folder(output_folder, ".mp3")
    
    if not file_list:
        print(f"Нет mp3 файлов в {output_folder}")
        return
    
    for i, file_name in enumerate(file_list):
        part_name = i + 1
        out_file_name = os.path.join(output_folder, f"{os.path.basename(output_folder)}_part{part_name}.txt")
        
        whisper_net = Whisperlocal(log_file, out_file_name)

        print(f"Обработка файла: {file_name}")
        print(f"output_folder: {output_folder}")
        print(f"сохраним сюда: {out_file_name}")
        
        start_time = i * parts_time + initial_time
        process_file(file_name, start_time, output_folder, whisper_net)

    file_list_txt = txt.sort_files_in_folder(output_folder, ".txt")
    TextFileReader.assemble(file_list_txt, output_folder, log_file)
    print(f"Готово: {log_file}")

    # Подключаемся к FTP
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user_name, passwd=ftp_password)
    ftp.cwd(ftp_path)  # переходим в нужную директорию на FTP
    with open(log_file, 'rb') as f:
        # Имя файла на FTP будет таким же, как локальное имя
        filename = log_file.split('/')[-1]  # или os.path.basename(file_path)
        #print(f"Загружаем файл {filename} на FTP...")
        print(f"https://podvi.ru/n8n/{filename}")
        ftp.storbinary(f'STOR {filename}', f)
        ftp.quit()
    # Отправляем письмо
    send_email(filename)   
if __name__ == "__main__":
    folder = args.input_folder if args.input_folder else input_folder
    print(f"Взята в обработку папка: {folder}")
    main(folder)