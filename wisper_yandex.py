from classes.YandexSpeechkitClient import YandexSpeechkitClient
from classes.TextFileReader import TextFileReader
import threading

output_folder = '07.26_5_4floor_11.00(01.14)'

parts_time=600
initial_time = 0
segments = 12
log_file = output_folder + ".txt" # »м¤ файлика с результатом с переносами строк
# out_file_name = "out.txt"
max_threads = 50
thread_semaphore = threading.BoundedSemaphore(value=max_threads)


txt = TextFileReader("")
file_list = txt.sort_files_in_folder(output_folder, ".mp3")


# whisper = YandexSpeechkitClient(log_file)
#
# start_time=initial_time


print("Привет")

def process_file(file_name, start_time, whisper, output_folder):
    # whisper.transcribe_audio(f"{output_folder}/{file_name}")
    # whisper.segments_text(start_time, segments, output_folder)
    whisper.transcribe_audio(f"{output_folder}/{file_name}")
    whisper.segments_text(start_time,output_folder)

# Now file_list contains the names of all files sorted by part number
i=0
threads = []
for file_name in file_list:
    part_name=i+1
    out_file_name = f"{output_folder}/{output_folder}_part{part_name}.txt"
    whisper = YandexSpeechkitClient(log_file,out_file_name)
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