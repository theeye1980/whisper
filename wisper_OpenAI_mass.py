# 1. Расклеиваем выходной файл на части размером не более 24 Мб, все части нумеруем и сохрянем во временной папке с именем, как имя файла
# 2. Транскрибируем каждую часть и записываем все части в единый текстовый журнал для обработки.
import threading
from classes.OpenAIClient import OpenAIClient
from classes.TextFileReader import TextFileReader
import os



# Semaphore to limit the number of concurrent threads
max_threads = 50
thread_semaphore = threading.BoundedSemaphore(value=max_threads)

def process_file(file_name, start_time, whisper, output_folder):
    try:
        whisper.transcribe_audio(f"{output_folder}/{file_name}")
        whisper.segments_text(start_time, segments, output_folder)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
    finally:
        thread_semaphore.release()  # Ensure semaphore is released


# Собираем информацию о проектах

txt = TextFileReader("")
projects = txt.scan_folders(".")

for project in projects:
    output_folder = project  # Папка, в которой лежат исходные расклеенные mp3 файлы
    parts_time = 600
    initial_time = 0
    log_file = output_folder + ".txt"  # Имя файлика с результатом с переносами строк
    log_file_all = output_folder + "_2.txt"  # Имя файлика с результатами без переноса строк
    segments = 12

    #Считываем все расклеенные файлики
    #Перебираем каждый файлик от начала и до конца и отправляем каждый из них на транскрибацию и записываем результат

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