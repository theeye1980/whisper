from openai import OpenAI
import datetime
class OpenAIClient:
    def __init__(self, log_file):
        self.client = OpenAI(

                )
        self.transcription_result = None
        self.log_file = log_file
        self.audio_file_path = None

    def transcribe_audio(self, audio_file_path):
        audio_file = open(audio_file_path, "rb")
        self.transcription_result = self.client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
        return self.transcription_result

    def segments_text(self,start_time):
        new_timeline_need = True
        for segment in self.transcription_result.model_extra['segments']:
            start = segment['start'] + start_time

            start = round(start)

            hours = int(start // 3600)
            minutes = int((start % 3600) // 60)
            seconds = int(start % 60)

            time_format = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
            start_str = str(time_format)

            text = segment['text']
            print('Start:', start_str, 'Text:', text)
            if new_timeline_need:
                out = start_str + '::' + text
            else:
                out=text

            self.save_string_to_file(self.log_file, out)

            # Проверем, нужно ли в следующий раз указывать тайминг при записи
            new_timeline_need = self.check_string(text)

            start_str = ''
            text = ''


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


