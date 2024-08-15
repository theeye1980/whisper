# 1. Расклеиваем выходной файл на части размером не более 24 Мб, все части нумеруем и сохрянем во временной папке с именем, как имя файла
# 2. Транскрибируем каждую часть и записываем все части в единый текстовый журнал для обработки.
import threading
from classes.OpenAIClient import OpenAIClient
from classes.TextFileReader import TextFileReader
import os

output_folder = "06.25_3_Zal_Soveta_14.00(03.34)" #Папка, в которой лежат исходные расклеенные mp3 файлы
parts_time=600
initial_time = 0
log_file = output_folder + ".txt" # Имя файлика с результатом с переносами строк
log_file_all = output_folder + "_2.txt"    #Имя файлика с результатами без переноса строк
segments = 12

# Semaphore to limit the number of concurrent threads
max_threads = 50
thread_semaphore = threading.BoundedSemaphore(value=max_threads)

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
# 1. Расклеиваем выходной файл на части размером не более 24 Мб, все части нумеруем и сохрянем во временной папке с именем, как имя файла
# 2. Транскрибируем каждую часть и записываем все части в единый текстовый журнал для обработки.
import threading
from classes.OpenAIClient import OpenAIClient
from classes.TextFileReader import TextFileReader
import os

output_folder = "08.14_4_4floor_11.30(02.26)" #Папка, в которой лежат исходные расклеенные mp3 файлы
parts_time=600
initial_time = 0
log_file = output_folder + ".txt" # Имя файлика с результатом с переносами строк
log_file_all = output_folder + "_2.txt"    #Имя файлика с результатами без переноса строк
segments = 12

# Semaphore to limit the number of concurrent threads
max_threads = 50
thread_semaphore = threading.BoundedSemaphore(value=max_threads)

def process_file(file_name, start_time, whisper, output_folder):
    whisper.transcribe_audio(f"{output_folder}/{file_name}")
    whisper.segments_text(start_time, segments, output_folder)

#Считываем все расклеенные файлики
#Перебираем каждый файлик от начала и до конца и отправляем каждый из них на транскрибацию и записываем результат

txt = TextFileReader("")

file_list = txt.sort_files_in_folder(output_folder, ".mp3")

# Now file_list contains the names of all files sorted by part number
i=0
threads = []
for file_name in file_list:
    part_name=i+1
    out_file_name = f"{output_folder}/{output_folder}_part{part_name}.txt"
    whisper = OpenAIClient(log_file, out_file_name)
    print(file_name)
    start_time=i*parts_time + initial_time
    i = i + 1

    # Acquire semaphore before starting the thread
    thread_semaphore.acquire()

    # Create a thread for processing the file
    t = threading.Thread(target=process_file, args=(file_name, start_time, whisper, output_folder))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
print("Уходите!")

# Соберем все кусочки текстовых файлов в единый файл
file_list = txt.sort_files_in_folder(output_folder, ".txt")
TextFileReader.assemble(file_list,output_folder,log_file)
# Sort the file list based on the part number in the file name
file_list.sort(key=lambda x: int(x.split("_part")[1].split(".")[0]))


whisper = OpenAIClient(log_file)

# Now file_list contains the names of all files sorted by part number
i=0
for file_name in file_list:
    print(file_name)
    start_time=i*parts_time
    whisper.transcribe_audio(f"{output_folder}/{file_name}")
    whisper.segments_text(start_time)
    i=i+1


txt = TextFileReader("")

file_list = txt.sort_files_in_folder(output_folder, ".mp3")

# Now file_list contains the names of all files sorted by part number
i=0
threads = []
for file_name in file_list:
    part_name=i+1
    out_file_name = f"{output_folder}/{output_folder}_part{part_name}.txt"
    whisper = OpenAIClient(log_file, out_file_name)
    print(file_name)
    start_time=i*parts_time + initial_time
    i = i + 1

    # Acquire semaphore before starting the thread
    thread_semaphore.acquire()

    # Create a thread for processing the file
    t = threading.Thread(target=process_file, args=(file_name, start_time, whisper, output_folder))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
print("Уходите!")

# Соберем все кусочки текстовых файлов в единый файл
file_list = txt.sort_files_in_folder(output_folder, ".txt")
TextFileReader.assemble(file_list,output_folder,log_file)

