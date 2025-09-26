from classes.TextFileReader import TextFileReader
import shutil

txt = TextFileReader("")
projects = txt.scan_folders(".")

for project in projects:
    print(project)
    shutil.rmtree(project)

txt.delete_old_projects_files(".")