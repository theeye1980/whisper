# Запускаем, когда какие-то txt файлы по любым причинам не создались к частям
import os
import threading
from classes.OpenAIClient import OpenAIClient
# from classes.YandexSpeechkitClient import YandexSpeechkitClient
from classes.Whisperlocal import Whisperlocal
import whisper
from classes.TextFileReader import TextFileReader
segments = 12
parts_time = 600



# Собираем папки проектов
txt = TextFileReader("")
projects = txt.scan_folders(".")

# ищем файлы mp3, для которых отсутствует txt с таким же названием
files_to_repair = txt.find_mp3_without_txt(projects)

def process_file(file_name, start_time, whisper, output_folder, language='ru'):
    try:
        result = whisper_model.transcribe(
            os.path.join(output_folder, file_name),
            language=language  # Здесь указываем язык
        )
        whisper_net.segments_text(start_time, segments, result)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")



threads = []
i=0
for file in files_to_repair:
    print (file)
    log_file = f"{i}.txt"
    new_file_path = file.replace(".mp3", ".txt")

    whisper_net = Whisperlocal(log_file, new_file_path)
    # whisper = YandexSpeechkitClient(log_file, new_file_path)

    #определим start_time
    part_num = txt.extract_part_number(new_file_path)
    start_time = parts_time * (part_num - 1)

    # Acquire semaphore before starting the thread

    # Create a thread for processing the file
