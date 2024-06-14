from flask import Flask, request, render_template, jsonify, g
from classes.TextFileReader import TextFileReader
import os

app = Flask(__name__, template_folder='templates')
txt = TextFileReader("")

projects = txt.scan_folders(".")

problems = []
mp3 = []  # List to store lists of MP3 files for each project
txtc = []
i = 0  # Initialize the index variable

for project in projects:
    print(project)
    mp3files = txt.sort_files_in_folder(project, ".mp3")
    txtfiles = txt.sort_files_in_folder(project, ".txt")
    mp3.append(len(mp3files))  # Append the list of MP3 files for the current project to the main list
    txtc.append(len(txtfiles))

    #посчитаем число проблем и выделим файлы с проблемами

    isProblem = False

    for txtfile in txtfiles:
        file_path = os.path.join(project, txtfile)
        isProblem = False
        with open(file_path, "r") as input_file:
            content = input_file.read()
            dot_count, comma_count, uppercase_count = txt.count_characters(content)

        if dot_count < 10 or comma_count < 10 or uppercase_count < 10:
            isProblem = True

        print(f"{dot_count}, {comma_count}, {uppercase_count} - {isProblem}")

    i += 1

combined_list = zip(projects, mp3, txtc)
# считаем число текстовых фалов

# определяем файлы с проблемами


@app.route('/', methods=['GET', 'POST'])
def home():
    template = 'input.html'



    return render_template(template, display='none', displayalert='none', combined_list=combined_list, data = mp3)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)
