from classes.TextFileReader import TextFileReader
import os

txt = TextFileReader("")
projects = txt.scan_folders(".")

problem_files = txt.problems_find(projects)

with open("problem_files.txt", "w", encoding="utf-8") as file:
    for string in problem_files:
        file.write(string + "\n")