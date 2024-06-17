from classes.TextFileReader import TextFileReader
import os

txt = TextFileReader("")
projects = txt.scan_folders(".")

problem_files = []

for project in projects:
    print(project)
    mp3files = txt.sort_files_in_folder(project, ".mp3")
    txtfiles = txt.sort_files_in_folder(project, ".txt")

    #посчитаем число проблем и выделим файлы с проблемами
    problem_count=0
    for txtfile in txtfiles:
        file_path = os.path.join(project, txtfile)
        isProblem = False
        with open(file_path, "r") as input_file:
            content = input_file.read()
            dot_count, comma_count, uppercase_count = txt.count_characters(content)

        if dot_count < 10 or comma_count < 10 or uppercase_count < 10:
            isProblem = True
            problem_count+=1
            print(f"{txtfile}: {dot_count}, {comma_count}, {uppercase_count}")
            path = f"{project}/{txtfile}"
            problem_files.append(path)

with open("problem_files.txt", "w", encoding="utf-8") as file:
    for string in problem_files:
        file.write(string + "\n")