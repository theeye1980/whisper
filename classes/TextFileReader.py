class TextFileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text_chunks = []

    def read_file_and_split_chunks(self):
        temp_chunk = ""
        with open(self.file_path, 'r', encoding='cp1251') as file:
            for line in file:
                line = line.strip()
                if len(temp_chunk) + len(line) <= 4000:
                    temp_chunk += line + '\r\n'
                else:
                    self.text_chunks.append(temp_chunk)
                    temp_chunk = line + '\r\n'

        if temp_chunk:  # If there's any remaining text in temp_chunk
            self.text_chunks.append(temp_chunk)

        return self.text_chunks

    def save_string_to_file(self, file_path, input_string):
        with open(file_path, 'a') as file:
            # file.write('\nDate and Time: {}\n'.format(current_datetime))
            try:
                # Your code that might raise UnicodeEncodeError
                file.write(input_string)
            except UnicodeEncodeError as e:
                # Handle the exception (e.g., print an error message)
                print("UnicodeEncodeError occurred: {}".format(e))
                # Additional error handling code can be added here

