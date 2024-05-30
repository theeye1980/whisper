from pyannote.audio import Pipeline
from classes.bd import bdSQLite
from classes.config import DIA
import os

# задаем папку, по которой нужно определить смену спикеров
output_folder = "05.22_7_4floor_14.00(02.58)"
parts_time=600
initial_time = 0


pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=DIA)

# send pipeline to GPU (when available)
import torch
print(torch.cuda.is_available())

pipeline.to(torch.device("cuda"))

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
for file_name in file_list:
    print(file_name)
    file_path = f"{output_folder}/{file_name}"


    # apply pretrained pipeline
    diarization = pipeline(file_path)

    db = bdSQLite()
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start_time = i * parts_time + initial_time
        result = f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}"
        print(f"Временная метка {turn.start}, спикер {speaker}")
        real_time = start_time + turn.start

        db.insert_speaker_data(1,speaker,real_time)

        # Print the result to the console
        print(result)

    # Empty the diarization variable
    diarization = None
    i=i+1




