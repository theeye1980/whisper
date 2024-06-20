from classes.OpenAIClient import OpenAIClient
from classes.TextFileReader import TextFileReader
import os

output_folder = "06.19_5_Zom3_15.00(02.34)" #Папка, в которой лежат исходные текстовые файлы
parts_time=600
initial_time = 0
log_file = output_folder + "_.txt" # Имя файлика с результатом с переносами строк
# log_file_all = output_folder + "_2.txt"    #Имя файлика с результатами без переноса строк


txt = TextFileReader("")
# Соберем все кусочки текстовых файлов в единый файл
file_list = txt.sort_files_in_folder(output_folder, ".txt")

# Соберем все кусочки текстовых файлов в единый файл
file_list = txt.sort_files_in_folder(output_folder, ".txt")

with open(log_file, "w") as output_file:
    for file_name in file_list:

        # Initialize counters for dots, commas, and uppercase letters
        dot_count = 0
        comma_count = 0
        uppercase_count = 0

        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "r") as input_file:
            content = input_file.read()

            dot_count, comma_count, uppercase_count = txt.count_characters(content)

            # Write the content to the output file
            output_file.write(content)

        # Output the statistics
        print(f"Статистика по файлу {file_name}: Точек: {dot_count}, Запятых: {comma_count}, Заглавных букв: {uppercase_count}")