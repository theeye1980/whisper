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
        for segment in self.transcription_result.model_extra['segments']:
            start = segment['start'] + start_time
            start = round(start)
            start_str = str(start)
            text = segment['text']
            print('Start:', start, 'Text:', text)
            out = start_str + '::' + text
            self.save_string_to_file(self.log_file, out)
            start_str = ''
            text = ''

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

# # Example usage
# client = OpenAIClient()
# transcription = client.transcribe_audio("Test_10m.mp3")
# print(transcription)
