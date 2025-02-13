from classes.OpenAIClient import OpenAIClient
from classes.TextFileReader import TextFileReader
import os

output_folder = "06.20_5_5floor_15.00(00.52)" #Папка, в которой лежат исходные текстовые файлы
parts_time=600
initial_time = 0
log_file = output_folder + "_.txt" # Имя файлика с результатом с переносами строк
# log_file_all = output_folder + "_2.txt"    #Имя файлика с результатами без переноса строк


txt = TextFileReader("")
# Соберем все кусочки текстовых файлов в единый файл
file_list = txt.sort_files_in_folder(output_folder, ".txt")

# Соберем все кусочки текстовых файлов в единый файл
file_list = txt.sort_files_in_folder(output_folder, ".txt")

TextFileReader.assemble(file_list,output_folder,log_file)