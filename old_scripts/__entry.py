import csv
import re


def extract_date(line):
    """
    Extracts the date from the third line of the block.
    Assumes the date is in the format 'dd.mm' before an underscore.
    """
    match = re.search(r'\b\d{2}\.\d{2}\.\d{4}\b', line)
    return match.group(0) if match else ''


def get_duration_minutes(filename):
    # Ищем в имени файла часть в скобках, например (03.56)
    match = re.search(r'\((\d{2})\.(\d{2})\)', filename)
    if not match:
        raise ValueError("Длительность в нужном формате не найдена в имени файла")

    hours = int(match.group(1))
    minutes = int(match.group(2))

    total_minutes = hours * 60 + minutes
    return total_minutes

def process_text_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    blocks = []
    link = ''
    current_block = []

    # Process the input file line by line
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  # Skip empty lines
            current_block.append(stripped_line)
            if len(current_block) == 4:  # Collect blocks of exactly 4 lines
                blocks.append(current_block)
                current_block = []
        else:
            # Reset the current block if an empty line is encountered
            # current_block = []
            print ("Строка пустая, пропустим")

    # Capture the last line as the link
    if lines:
        last_line = lines[-1].strip()
        if last_line.startswith("Ссылка на записи:"):
            link = last_line.split(":", 1)[1].strip()

    # Write the output to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')

        # Write the header
        csv_writer.writerow(['Fourth Line', 'Second Line', 'First Line', 'Date', 'Duration','Link'])

        # Process each block and write to the CSV
        for block in blocks:
            if len(block) == 4:
                fourth_line = block[3]
                second_line = block[1]
                first_line = block[0]
                date = extract_date(block[2])
                duration = get_duration_minutes(block[1])
                csv_writer.writerow([fourth_line, second_line, first_line, date, duration, link])


# Example usage
input_file = 'input.txt'  # Replace with your input file name
output_file = 'output.csv'  # Replace with your desired output file name
process_text_file(input_file, output_file)