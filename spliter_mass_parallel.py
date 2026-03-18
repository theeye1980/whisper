import argparse
from pydub import AudioSegment
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, '/home/vyacheslav/projects/whisper')
from config import input_folder as config_input_folder, parts_time
from rabbit_utils import send_to_whisper

def split_mp3(file_path, max_length, output_folder1):
    audio = AudioSegment.from_file(file_path, format="mp3")
    file_name = os.path.basename(file_path)

    if not os.path.exists(output_folder1):
        os.makedirs(output_folder1)

    num_parts = len(audio) // (max_length * 1000) + 1

    for i in range(num_parts):
        start_time = i * max_length * 1000
        end_time = min((i + 1) * max_length * 1000, len(audio))
        part = audio[start_time:end_time]
        part.export(os.path.join(output_folder1, f"{os.path.splitext(file_name)[0]}_part{i + 1}.mp3"), format="mp3")
    
    return output_folder1  # Возвращаем путь к папке с частями


def process_file(file_named, folder):
    if file_named.endswith(".mp3"):
        audio_file_path = os.path.join(folder, file_named)
        output_folder = os.path.join(folder, file_named[:-4])
        split_mp3(audio_file_path, parts_time, output_folder)
    
        return output_folder 
    return None 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder', type=str, default=None)
    args = parser.parse_args()

    folder = args.input_folder if args.input_folder else config_input_folder
    
    print(f"Взята в обработку папка: {folder}")

    start_time = time.time()
    file_list = [f for f in os.listdir(folder) if f.endswith(".mp3")]
    
    print(f"Найдено файлов: {len(file_list)}")

    with ProcessPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(process_file, file_list, [folder] * len(file_list)))
    
        # Отправляем задания в очередь stage_whisper
    for output_folder in results:
        if output_folder:
            send_to_whisper(output_folder)

    print(f"Total time taken: {time.time() - start_time:.2f} seconds")