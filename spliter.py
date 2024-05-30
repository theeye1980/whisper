from pydub import AudioSegment
import os

AudioFilePath = "05.22_7_4floor_14.00(02.58).mp3"
output_folder = AudioFilePath[:-4]
parts_time=600

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


split_mp3(AudioFilePath, parts_time, output_folder)