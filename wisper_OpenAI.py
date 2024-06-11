# 1. Расклеиваем выходной файл на части размером не более 24 Мб, все части нумеруем и сохрянем во временной папке с именем, как имя файла
# 2. Транскрибируем каждую часть и записываем все части в единый текстовый журнал для обработки.
import threading
from classes.OpenAIClient import OpenAIClient
import os

output_folder = "test" #Папка, в которой лежат исходные расклеенные mp3 файлы
parts_time=600
initial_time = 0
log_file = output_folder + ".txt" # Имя файлика с результатом с переносами строк
log_file_all = output_folder + "_2.txt"    #Имя файлика с результатами без переноса строк
segments = 12

def process_file(file_name, start_time, whisper, output_folder):
    whisper.transcribe_audio(f"{output_folder}/{file_name}")
    whisper.segments_text(start_time, segments, output_folder)

#Считываем все расклеенные файлики
#Перебираем каждый файлик от начала и до конца и отправляем каждый из них на транскрибацию и записываем результат

file_list = []
# Iterate over all files in the folder
for file_name in os.listdir(output_folder):
    if file_name.endswith(".mp3"):
        file_list.append(file_name)

# Sort the file list based on the part number in the file name
file_list.sort(key=lambda x: int(x.split("_part")[1].split(".")[0]))



# Now file_list contains the names of all files sorted by part number
i=0
threads = []
for file_name in file_list:
    out_file_name = f"{output_folder}/{output_folder}_part{i}.txt"
    whisper = OpenAIClient(log_file, out_file_name)
    print(file_name)
    start_time=i*parts_time + initial_time
    i = i + 1

    # Create a thread for processing the file
    t = threading.Thread(target=process_file, args=(file_name, start_time, whisper, output_folder))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
print("Уходите!")


