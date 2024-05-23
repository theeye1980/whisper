# 1. Расклеиваем выходной файл на части размером не более 24 Мб, все части нумеруем и сохрянем во временной папке с именем, как имя файла
# 2. Транскрибируем каждую часть и записываем все части в единый текстовый журнал для обработки.

from classes.OpenAIClient import OpenAIClient
import os

output_folder = "brazil" #Папка, в которой лежат исходные расклеенные mp3 файлы
parts_time=600
initial_time = 0
log_file = "brazil.txt" # Имя файлика с результатом с переносами строк
log_file_all = "brazil_2.txt"    #Имя файлика с результатами без переноса строк
segments = 8


#Считываем все расклеенные файлики
#Перебираем каждый файлик от начала и до конца и отправляем каждый из них на транскрибацию и записываем результат

file_list = []
# Iterate over all files in the folder
for file_name in os.listdir(output_folder):
    if file_name.endswith(".mp3"):
        file_list.append(file_name)

# Sort the file list based on the part number in the file name
file_list.sort(key=lambda x: int(x.split("_part")[1].split(".")[0]))


whisper = OpenAIClient(log_file,log_file_all)

# Now file_list contains the names of all files sorted by part number
i=0
for file_name in file_list:
    print(file_name)
    start_time=i*parts_time + initial_time
    whisper.transcribe_audio(f"{output_folder}/{file_name}")
    whisper.segments_text(start_time,segments)
    i=i+1




