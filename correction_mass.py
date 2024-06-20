# запускает автоматический сбор и коррекцию всех проблемных файлов
from classes.TextFileReader import TextFileReader
from classes.OpenAIChatbot import OpenAIChatbot
import json
import os

# Собираем информацию о проблемных файлах

txt = TextFileReader("")
projects = txt.scan_folders(".")

projects = txt.scan_folders(".")

problem_paths = []
problem_files = []

chatbot = OpenAIChatbot()
model = "gpt-3.5-turbo"
temperatura = 0.1
helper = "Analyze the text below. Add commas and periods, as well as capitalize where appropriate.  Do not change or add anything else:"

def correcion(chunks, file_path ):
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
        text_reader.save_string_to_file(file_path, corrected_chunk)


for project in projects:
    print(project)
    txtfiles = txt.sort_files_in_folder(project, ".txt")

    #посчитаем число проблем и выделим файлы с проблемами
    problem_count=0
    for txtfile in txtfiles:
        file_path = os.path.join(project, txtfile)

        with open(file_path, "r") as input_file:
            content = input_file.read()
            dot_count, comma_count, uppercase_count = txt.count_characters(content)

        if dot_count < 10 or comma_count < 10 or uppercase_count < 10:
            problem_files.append(txtfile)
            problem_paths.append(file_path)
            print(f"{txtfile} - {dot_count}, {comma_count}, {uppercase_count} ")

            # запускаем коррекцию файла
            text_reader = TextFileReader(file_path)
            # получаем чанки файла
            chunks = text_reader.read_file_and_split_chunks()

            # проделываем коррекцию
            correcion(chunks,txtfile)


