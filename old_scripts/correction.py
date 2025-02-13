from classes.TextFileReader import TextFileReader
from classes.OpenAIChatbot import OpenAIChatbot
import json

# Example usage
file_path = "06.19_5_Zom3_15.00(02.34)_part7.txt" # входной файл
file_out = f"{file_path}_orig_copy.txt" # выходной файл
text_reader = TextFileReader(file_path)

# Сохраним копию файла

text_reader.copy_file(file_path, file_out)

# получаем чанки файла
chunks = text_reader.read_file_and_split_chunks()


# Прогоняем по chatGPT и просим помощи

chatbot = OpenAIChatbot()
model = "gpt-3.5-turbo"
temperatura = 0.1
helper = "Analyze the text below. Add commas and periods, as well as capitalize where appropriate.  Do not change or add anything else:"

# Print the chunks
for idx, chunk in enumerate(chunks):

    promt = helper + chunk
    resp = chatbot.get_response(promt, model, temperatura)

    # load the json string
    data = json.loads(resp)

    # print the content
    print(data['choices'][0]['message']['content'])

    corrected_chunk = data['choices'][0]['message']['content']
    text_reader.save_string_to_file(file_path, corrected_chunk)

