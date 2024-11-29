from pydub import AudioSegment
import os

def split_mp3(file_path, max_length, output_folder1):
    audio = AudioSegment.from_file(file_path, format="mp3")
    file_name = os.path.basename(file_path)

    if not os.path.exists(output_folder1):
        os.mkdir(output_folder1)

    num_parts = len(audio) // (max_length * 1000) + 1

    for i in range(num_parts):
        start_time = i * max_length * 1000
        end_time = min((i + 1) * max_length * 1000, len(audio))
        part = audio[start_time:end_time]
        part.export(os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_part{i + 1}.mp3"), format="mp3")

# Указываем входную папку (полный путь)
input_folder = r"/home/vyacheslav/Загрузки/Стенограммы_27.11.2024"

# Get audio files from the folder
file_list = []
# Iterate over all files in the folder
for file_named in os.listdir(input_folder):
    if file_named.endswith(".mp3"):
        AudioFilePath = os.path.join(input_folder, file_named)
        output_folder = file_named[:-4]  # Create output folder in the same directory
        parts_time = 600  # Length of each part in seconds
        split_mp3(AudioFilePath, parts_time, output_folder)








