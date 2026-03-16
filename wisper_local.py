from classes.Whisperlocal import Whisperlocal
from faster_whisper import WhisperModel
from classes.TextFileReader import TextFileReader
import os
import torch
import requests
import time
from config import output_folder, parts_time, initial_time, segments, url, chat_id


print(torch.cuda.is_available())
print(torch.cuda.current_device())
print(torch.cuda.get_device_name(torch.cuda.current_device()))

whisper_model = WhisperModel("large-v3", device="cuda", compute_type="float16")


def process_file(file_name, start_time, output_folder, language='ru'):
    try:
        chunk_start = time.time()

        segments_result, info = whisper_model.transcribe(
            os.path.join(output_folder, file_name),
            language=language,
            beam_size=1,
            condition_on_previous_text=False,
            vad_filter=True,  # добавить VAD фильтр
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        # faster-whisper возвращает генератор, конвертируем в список
        segments_list = list(segments_result)

        chunk_time = time.time() - chunk_start
        whisper_net.segments_text(start_time, segments, segments_list)
        print(f"Обработано за {chunk_time:.2f} сек")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")


txt = TextFileReader("")
projects = txt.scan_folders(".")

for project in projects:
    output_folder = project
    log_file = output_folder + ".txt"
    log_file_all = output_folder + "_2.txt"

    file_list = txt.sort_files_in_folder(output_folder, ".mp3")
    i = 0

    for file_name in file_list:
        part_name = i + 1
        out_file_name = os.path.join(output_folder, f"{output_folder}_part{part_name}.txt")
        whisper_net = Whisperlocal(log_file, out_file_name)

        print(file_name)
        start_time = i * parts_time + initial_time
        i = i + 1

        process_file(file_name, start_time, output_folder)

    print("Уходите!")

    file_list = txt.sort_files_in_folder(output_folder, ".txt")
    TextFileReader.assemble(file_list, output_folder, log_file)

payload = {
    'chat_id': chat_id,
    'text': "Усё готово! проверяй"
}

# response = session.post(url, data=payload, timeout=30)
