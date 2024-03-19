# 1. Расклеиваем выходной файл на части размером не более 24 Мб, все части нумеруем и сохрянем во временной папке с именем, как имя файла
# 2. Транскрибируем каждую часть и записываем все части в единый текстовый журнал для обработки.
from pydub import AudioSegment
from classes.OpenAIClient import OpenAIClient
import os

AudioFilePath = "test_big_part4.mp3"
output_folder = "split_files_900"
log_file = "test_big_900.txt"
parts_time=900


def split_mp3(file_name, max_length, output_folder):
    audio = AudioSegment.from_file(file_name, format="mp3")

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    num_parts = len(audio) // (max_length * 1000) + 1

    for i in range(num_parts):
        start_time = i * max_length * 1000
        end_time = min((i + 1) * max_length * 1000, len(audio))
        part = audio[start_time:end_time]
        part.export(f"{output_folder}/{os.path.splitext(file_name)[0]}_part{i + 1}.mp3", format="mp3")

# split_mp3(AudioFilePath, parts_time, output_folder)

#Считываем все расклеенные файлики
#Перебираем каждый файлик от начала и до конца и отправляем каждый из них на транскрибацию и записываем результат

file_list = []
# Iterate over all files in the folder
for file_name in os.listdir(output_folder):
    if file_name.endswith(".mp3"):
        file_list.append(file_name)

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




