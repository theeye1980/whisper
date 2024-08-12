from classes.YandexSpeechkitClient import YandexSpeechkitClient
from classes.TextFileReader import TextFileReader

output_file = '07.26_5_4floor_11.00(01.14)/07.26_5_4floor_11.00(01.14)_part8.mp3'

parts_time=600
initial_time = 0
segments = 12
log_file = output_file + ".txt" # »м¤ файлика с результатом с переносами строк
out_file_name = "out.txt"
whisper = YandexSpeechkitClient(log_file)

result = whisper.transcribe_audio(output_file)
start_time=initial_time
whisper.segments_text(start_time)

#
# for c, res in enumerate(result):
#     print(f'channel: {c}\n'
#           f'raw_text: {res.raw_text}\n'
#           f'norm_text: {res.normalized_text}\n')
#
# for c, res in enumerate(result):
#     print(f'channel: {c}')
#     for utterance in res.utterances:
#         print(utterance)

print("Привет")