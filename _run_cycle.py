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
    response = requests.post(url, json=payload)
    return response.json()

# Запускает производство полного цикла

# Step 1 - split files
subprocess.run(['python', 'spliter_mass_parallel.py'], capture_output=True, text=True)
# Step 2 - check splited files

txt = TextFileReader("")
projects = txt.scan_folders(".")

for project in projects:
    print(project)
    txtfiles = txt.sort_files_in_folder(project, ".mp3")
    num_files = len(txtfiles)
    message = f"{project} \n число расклеенных файлов {num_files}"
    send_telegram_message(message)

# Step 3 - start mass transcribe
subprocess.run(['python', 'wisper_OpenAI_mass.py'], capture_output=True, text=True)

# Step 4 - check transcribed files
# ищем файлы mp3, для которых отсутствует txt с таким же названием
files_to_repair = txt.find_mp3_without_txt(projects)

if files_to_repair==None:
    message_content = "Все файлы распознаны, переходим к проверке"
    send_telegram_message(message_content)
else:
    message_content = "\n".join(files_to_repair)
    send_telegram_message(message_content)

# Step 5 - run repair just in case
subprocess.run(['python', 'repair.py'], capture_output=True, text=True)

# Step 6 - check transcribed files
# ищем файлы mp3, для которых отсутствует txt с таким же названием
files_to_repair = txt.find_mp3_without_txt(projects)

if files_to_repair==None:
    message_content = "Все файлы распознаны, ищем проблемы со знаками препинания"
    send_telegram_message(message_content)
else:
    message_content = "\n".join(files_to_repair)
    send_telegram_message(message_content)
    message_content = "Нужна ручная проверка. Что-то не то"

    send_telegram_message(message_content)
    sys.exit()

print ("это не должно быть напечатано")

# Step 6 - check problems with txt - try to correction_mass

subprocess.run(['python', 'correction_mass_fast.py'], capture_output=True, text=True)

message_content = "Вроде все, нужно в ручном режиме посмотреть на кусочки и запустить пересборку"
send_telegram_message(message_content)