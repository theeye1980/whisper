# запускает пересборку текстовых файлов в один со всех проектов
from classes.TextFileReader import TextFileReader
import os

# Собираем информацию о проблемных файлах

txt = TextFileReader("")
projects = txt.scan_folders(".")

for project in projects:
    print(project)
    txtfiles = txt.sort_files_in_folder(project, ".txt")
    print('hi')
    log_file = project + "_.txt"
    TextFileReader.assemble(txtfiles, project, log_file)
  