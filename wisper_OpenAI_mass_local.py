# 1. Расклеиваем выходной файл на части размером не более 24 Мб, все части нумеруем и сохрянем во временной папке с именем, как имя файла
# 2. Транскрибируем каждую часть и записываем все части в единый текстовый журнал для обработки.

from classes.Whisperlocal import Whisperlocal
import whisper
from classes.TextFileReader import TextFileReader
import os
import requests
from config import output_folder,parts_time,initial_time,segments, url, chat_id



whisper = whisper.load_model("turbo")

def process_file(file_name, start_time, whisper, output_folder):
    try:
        result = whisper.transcribe(os.path.join(output_folder, file_name))
        whisper_net.segments_text(start_time, segments, result)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")


# Собираем информацию о проектахКруглый стол «Создание и функционирование Научно-образовательного центра имени Н.Я. Данилевского в 2025 году»

txt = TextFileReader("")
projects = txt.scan_folders(".")

for project in projects:
    output_folder = project  # Папка, в которой лежат исходные расклеенные mp3 файлы
    # parts_time = 600
    # initial_time = 0
    log_file = output_folder + ".txt"  # Имя файлика с результатом с переносами строк
    log_file_all = output_folder + "_2.txt"  # Имя файлика с результатами без переноса строк
    # segments = 12

    #Считываем все расклеенные файлики
    #Перебираем каждый файлик от начала и до конца и отправляем каждый из них на транскрибацию и записываем результат

    file_list = txt.sort_files_in_folder(output_folder, ".mp3")

    # Now file_list contains the names of all files sorted by part number
    i=0

    for file_name in file_list:

        part_name=i+1
        # out_file_name = f"{output_folder}/{output_folder}_part{part_name}.txt"
        out_file_name = os.path.join(output_folder, f"{output_folder}_part{part_name}.txt")

        whisper_net = Whisperlocal(log_file, out_file_name)


        print(file_name)
        start_time=i*parts_time + initial_time
        i = i + 1

        process_file(file_name, start_time, whisper, output_folder)



        
    print("Уходите!")

    # Соберем все кусочки текстовых файлов в единый файл
    file_list = txt.sort_files_in_folder(output_folder, ".txt")
    TextFileReader.assemble(file_list,output_folder,log_file)


payload = {
        'chat_id': chat_id,
        'text': "Усё готово! проверяй"
    }

response = requests.post(url, data=payload)