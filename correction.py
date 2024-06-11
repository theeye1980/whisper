from classes.TextFileReader import TextFileReader
from classes.OpenAIChatbot import OpenAIChatbot
import json

# Example usage
file_path = "06.07_3_5floor_11.30(04.43)_3.txt" # входной файл
file_out = "06.07_3_5floor_11.30(04.43)_corrected.txt" # выходной файл
text_reader = TextFileReader(file_path)

# получаем чанки файла
chunks = text_reader.read_file_and_split_chunks()


# Прогоняем по chatGPT и просим помощи

chatbot = OpenAIChatbot()
model = "gpt-3.5-turbo"
temperatura = 0.1
helper = "Analyze the text below. Add commas and periods, as well as capitalize where appropriate.  Do not change or add anything else:"

# Print the chunks
for idx, chunk in enumerate(chunks):
    print(f"Chunk {idx + 1}:")
    print(chunk)
    print("----------")
    promt = helper + chunk

    resp = chatbot.get_response(promt, model, temperatura)
    print(resp)
    # load the json string
    data = json.loads(resp)

    print("Корректируем ----------")
    # print the content
    print(data['choices'][0]['message']['content'])

    corrected_chunk = data['choices'][0]['message']['content']
    text_reader.save_string_to_file(file_out, corrected_chunk)

