# Запускаем, когда какие-то txt файлы по любым причинам не создались к частям
import os
import threading
from classes.OpenAIClient import OpenAIClient
from classes.TextFileReader import TextFileReader
segments = 12
parts_time = 600

max_threads = os.cpu_count() * 2  # For example, use double the number of cores
thread_semaphore = threading.BoundedSemaphore(value=max_threads)
print(f"максимум потоков - {max_threads})")

# Собираем папки проектов
txt = TextFileReader("")
projects = txt.scan_folders(".")

# ищем файлы mp3, для которых отсутствует txt с таким же названием
files_to_repair = txt.find_mp3_without_txt(projects)

def process_file(file_path, start_time, whisper):
    try:
        dir_path = os.path.dirname(file_path)
        whisper.transcribe_audio(f"{file_path}")
        whisper.segments_text(start_time, segments, dir_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    finally:
        thread_semaphore.release()  # Ensure semaphore is released


threads = []
i=0
for file in files_to_repair:
    print (file)
    log_file = f"{i}.txt"
    new_file_path = file.replace(".mp3", ".txt")
    whisper = OpenAIClient(log_file, new_file_path)

    #определим start_time
    part_num = txt.extract_part_number(new_file_path)
    start_time = parts_time * (part_num - 1)

    # Acquire semaphore before starting the thread
    thread_semaphore.acquire()

    # Create a thread for processing the file
    t = threading.Thread(target=process_file, args=(file, start_time, whisper))
    threads.append(t)
    t.start()

    i += 1
    # Wait for all threads to complete
for t in threads:
    t.join()