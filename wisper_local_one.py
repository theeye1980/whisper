import os
import sys
import argparse
import torch
import requests
import time
from ftplib import FTP

sys.path.insert(0, '/home/vyacheslav/projects/whisper')

from faster_whisper import WhisperModel
from classes.Whisperlocal import Whisperlocal
from classes.TextFileReader import TextFileReader
from classes.EmailNotifier import EmailNotifier
from config import (
    input_folder, parts_time, initial_time, segments,
    ftp_path, ftp_host, ftp_user_name, ftp_password,
    SMTP_HOST, SMTP_PORT, EMAIL_ADDRESS, APP_PASSWORD,
    GOOGLE_DOCS_SHEET, GOOGLE_SHEET_WEBAPP_URL
)

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

    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user_name, passwd=ftp_password)
    ftp.cwd(ftp_path)
    with open(log_file, 'rb') as f:
        filename = os.path.basename(log_file)
        print(f"https://podvi.ru/n8n/{filename}")
        ftp.storbinary(f'STOR {filename}', f)

    ftp.quit()

    notifier = EmailNotifier(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        email_address=EMAIL_ADDRESS,
        app_password=APP_PASSWORD,
        default_to=[EMAIL_ADDRESS],  # уведомления себе
        #to=["kattyrinoa@mail.ru","v.kosarev@list.ru"]
    )
    notifier.send_link_notification(filename,to=["kattyrinoa@mail.ru","v.kosarev@list.ru"])
    
    filename_without_ext = filename[:-4]
    
    requests.post(
    GOOGLE_SHEET_WEBAPP_URL,
    json={
        "action": "setLinkByFilename",
        "filename": filename_without_ext,
        "link": f"https://podvi.ru/n8n/{filename}"
    },
    timeout=20
)

if __name__ == "__main__":
    folder = args.input_folder if args.input_folder else input_folder
    print(f"Взята в обработку папка: {folder}")
    main(folder)