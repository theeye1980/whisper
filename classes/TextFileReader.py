import datetime
import os
from typing import List
import re
class TextFileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text_chunks = []

    def read_file_and_split_chunks(self):
        temp_chunk = ""
        with open(self.file_path, 'r', encoding='cp1251') as file:
            for line in file:
                line = line.strip()
                if len(temp_chunk) + len(line) <= 10000:
                    temp_chunk += line + '\r\n'
                else:
                    self.text_chunks.append(temp_chunk)
                    temp_chunk = line + '\r\n'

        if temp_chunk:  # If there's any remaining text in temp_chunk
            self.text_chunks.append(temp_chunk)

        return self.text_chunks

    def ts_format(self, start):
        start = round(start)

        hours = int(start // 3600)
        minutes = int((start % 3600) // 60)
        seconds = int(start % 60)

        time_format = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        start_str = str(time_format)
        return start_str

    def check_string(self, input_string):
        # Trim leading and trailing spaces
        trimmed_string = input_string.strip()

        # Check if the last character is a dot
        if trimmed_string.endswith('.'):
            return True
        else:
            return False
    def sort_files_in_folder(self,output_folder, extention = ".mp3"):
        file_list = []
        # Iterate over all files in the folder
        for file_name in os.listdir(output_folder):
            if file_name.endswith(extention):
                file_list.append(file_name)

        # Sort the file list based on the part number in the file name
        file_list.sort(key=lambda x: int(x.split("_part")[1].split(".")[0]))
        return file_list

    def count_characters(self,content):
        dot_count = content.count('.')
        comma_count = content.count(',')
        uppercase_count = sum(1 for c in content if c.isupper())
        return dot_count, comma_count, uppercase_count

    def scan_folders(self, path):

        folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
        sorted_folders = sorted(folders)
        filtered_folders = [folder for folder in sorted_folders if folder not in ["classes", "reports", "templates", ".git", ".idea", '__pycache__']]
        return filtered_folders
    def copy_file(self, input, output):
        with open(input, 'r') as file:
            content = file.read()

        # Write the content to the copy file
        with open(output, 'w') as file:
            file.write(content)
    def problems_find(self, projects) -> List[str]:
        """
        Finds problematic files in the specified projects.

        Args:
        - projects (list): A list of project paths.

        Returns:
        - list of str: A list of paths to files identified as problematic.
        """
        problem_files = []
        for project in projects:
            txtfiles = self.sort_files_in_folder(project, ".txt")

            # посчитаем число проблем и выделим файлы с проблемами
            problem_count = 0
            for txtfile in txtfiles:
                file_path = os.path.join(project, txtfile)
                isProblem = False
                with open(file_path, "r") as input_file:
                    content = input_file.read()
                    dot_count, comma_count, uppercase_count = self.count_characters(content)

                if dot_count < 10 or comma_count < 10 or uppercase_count < 10:
                    isProblem = True
                    problem_count += 1
                    print(f"{txtfile}: {dot_count}, {comma_count}, {uppercase_count}")
                    path = f"{project}/{txtfile}"
                    problem_files.append(path)
        return  problem_files

    def find_mp3_without_txt(self, folders):
        missing_txt_files = []

        for folder in folders:
            # Get the full path of the folder
            folder_path = os.path.join(os.getcwd(), folder)

            # List all files in the folder
            files = os.listdir(folder_path)

            # Create sets for mp3 and txt files
            mp3_files = {file[:-4] for file in files if file.endswith('.mp3')}  # Remove the .mp3 extension
            txt_files = {file[:-4] for file in files if file.endswith('.txt')}  # Remove the .txt extension

            # Find mp3 files without corresponding txt files
            for mp3_file in mp3_files:
                if mp3_file not in txt_files:
                    missing_txt_files.append(os.path.join(folder, f"{mp3_file}.mp3"))

        # Report results
        if missing_txt_files:
            print(f"Found {len(missing_txt_files)} MP3 files without corresponding TXT files:")
            for mp3 in missing_txt_files:
                print(mp3)
            return missing_txt_files
        else:
            print("All MP3 files have corresponding TXT files. All is OK.")

    def extract_part_number(self, filename):
        # Use regex to find the part number in the filename
        match = re.search(r'_part(\d+)\.txt$', filename)
        if match:
            # Extract the number and convert it to an integer
            part_number = int(match.group(1))
            return part_number
        else:
            raise ValueError("No part number found in the filename.")
    @staticmethod
    def assemble(file_list, output_folder, log_file):
        txt = TextFileReader("")
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
                print(
                    f"Статистика по файлу {file_name}: Точек: {dot_count}, Запятых: {comma_count}, Заглавных букв: {uppercase_count}")

    def save_string_to_file(self, file_path, input_string):
        current_datetime = datetime.datetime.now()
        with open(file_path, 'a') as file:
            # file.write('\nDate and Time: {}\n'.format(current_datetime))
            try:
                # Your code that might raise UnicodeEncodeError
                file.write('\n' + input_string)
            except UnicodeEncodeError as e:
                # Handle the exception (e.g., print an error message)
                print("UnicodeEncodeError occurred: {}".format(e))
                # Additional error handling code can be added here