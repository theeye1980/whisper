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
    with open(log_file, "w") as output_file:
        for file_name in txtfiles:
            # Initialize counters for dots, commas, and uppercase letters
            dot_count = 0
            comma_count = 0
            uppercase_count = 0

            file_path = os.path.join(project, file_name)
            with open(file_path, "r") as input_file:
                content = input_file.read()

                dot_count, comma_count, uppercase_count = txt.count_characters(content)

                # Write the content to the output file
                output_file.write(content)

            # Output the statistics
            print(
                f"Summary {file_name}: dots: {dot_count}, commas: {comma_count}, Inline: {uppercase_count}")
