from speechkit import configure_credentials, creds
from speechkit import model_repository
from speechkit.stt import AudioProcessingType
from dotenv import load_dotenv
import os

import datetime
from classes.bd import bdSQLite

class YandexSpeechkitClient:
    def __init__(self, log_file):
        load_dotenv()
        config = {
            "YANDEX_API_KEY": os.getenv("YANDEX_API_KEY")
        }
        configure_credentials(
            yandex_credentials=creds.YandexCredentials(
                api_key=config['YANDEX_API_KEY']
            )
        )
        self.url = 'stt.api.cloud.yandex.net:443'
        self.model = model_repository.recognition_model()
        self.model.model = 'general'
        self.model.language = 'ru-RU'
        self.model.audio_processing_type = AudioProcessingType.Full
        self.transcription_result = None
        self.log_file = log_file
        self.audio_file_path = None

    def transcribe_audio(self, audio_file_path):
        self.transcription_result = self.model.transcribe_file(audio_file_path)
        return self.transcription_result

    def segments_text(self,start_time):

        all_text = '' # Задаем переменную для альтернативного текста
        db = bdSQLite()
        for segment in self.transcription_result:
            for seg in segment.utterances:

                print("stop")
                start = segment['start_time_ms'] + start_time
                st = start
                start = round(start)

                hours = int(start // 3600)
                minutes = int((start % 3600) // 60)
                seconds = int(start % 60)

                time_format = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
                start_str = str(time_format)

                text = segment['text']

                out = '\n' + start_str + ': ' + text
                all_text = all_text + " " + out

                # Обнулим на следующий проход
                start_str = ''
                text = ''

                segment_count=segment_count+1
        self.save_string_to_file("out.txt", all_text)

    def check_string(self, input_string):
        # Trim leading and trailing spaces
        trimmed_string = input_string.strip()

        # Check if the last character is a dot
        if trimmed_string.endswith('.'):
            return True
        else:
            return False


    def save_string_to_file(self, file_path, input_string):
        current_datetime = datetime.datetime.now()
        with open(file_path, 'a') as file:
            # file.write('\nDate and Time: {}\n'.format(current_datetime))
            try:
                # Your code that might raise UnicodeEncodeError
                file.write('\n' + input_string)
            except UnicodeEncodeError as e:
                # Handle the exception (e.g., print an error message)
                print("UnicodeEncodeError occurred: {}".format(e))
                # Additional error handling code can be added here

