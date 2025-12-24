import subprocess
import requests
import sys
from classes.TextFileReader import TextFileReader
from config import telegram_bot_token, telegram_chat_id

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    payload = {
        'chat_id': telegram_chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to send message: {e}")
        return None

# Запускает производство полного цикла

# Step 1 - split files
try:
    subprocess.run(['python', 'spliter_mass_parallel.py'], check=True)
except subprocess.CalledProcessError as e:
    error_message = f"Error in splitting files: {e}"
    send_telegram_message(error_message)
    sys.exit(1)

# Step 2 - check splitted files
txt = TextFileReader("")

try:
    projects = txt.scan_folders(".")
except Exception as e:
    send_telegram_message(f"Error scanning folders: {e}")
    sys.exit(1)

for project in projects:
    print(project)
    try:
        txtfiles = txt.sort_files_in_folder(project, ".mp3")
        num_files = len(txtfiles)
        message = f"{project} \n число расклеенных файлов {num_files}"
        send_telegram_message(message)
    except Exception as e:
        send_telegram_message(f"Error processing project {project}: {e}")

# Step 3 - start mass transcribe
try:
    subprocess.run(['python', 'wisper_OpenAI_mass.py'], check=True)
except subprocess.CalledProcessError as e:
    error_message = f"Error in mass transcription: {e}"
    send_telegram_message(error_message)
    sys.exit(1)

# Step 4 - check transcribed files
try:
    files_to_repair = txt.find_mp3_without_txt(projects)
except Exception as e:
    send_telegram_message(f"Error finding MP3 files without TXT: {e}")
    sys.exit(1)

if files_to_repair == None:
    message_content = "Все файлы распознаны, переходим к проверке"
    send_telegram_message(message_content)
else:
    message_content = "\n".join(files_to_repair)
    send_telegram_message(message_content)

# Step 5 - run repair just in case
try:
    subprocess.run(['python', 'repair.py'], check=True)
except subprocess.CalledProcessError as e:
    error_message = f"Error in repair process: {e}"
    send_telegram_message(error_message)
    sys.exit(1)

# Step 6 - check transcribed files
try:
    files_to_repair = txt.find_mp3_without_txt(projects)
except Exception as e:
    send_telegram_message(f"Error finding MP3 files without TXT during repair: {e}")
    sys.exit(1)

if files_to_repair == None:
    message_content = "Все файлы распознаны, ищем проблемы со знаками препинания"
    send_telegram_message(message_content)
else:
    message_content = "\n".join(files_to_repair)
    send_telegram_message(message_content)
    message_content = "Нужна ручная проверка. Что-то не то"
    send_telegram_message(message_content)
    sys.exit(1)

print("это не должно быть напечатано")

# Step 7 - check problems with txt - try to correction_mass
try:
    subprocess.run(['python', 'correction_mass_fast.py'], check=True)
except subprocess.CalledProcessError as e:
    error_message = f"Error in correction process: {e}"
    send_telegram_message(error_message)
    sys.exit(1)

message_content = "Вроде все, нужно в ручном режиме посмотреть на кусочки и запустить пересборку"
send_telegram_message(message_content)