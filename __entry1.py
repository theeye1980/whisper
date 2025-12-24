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
        content = infile.read()

    # Разделяем текст на секции "Срочные:" и "Обычные:"
    sections = {}

    # Находим секции
    urgent_match = re.search(r'Срочные:(.*?)(?=Обычные:|Ссылка на записи:|$)', content, re.DOTALL)
    regular_match = re.search(r'Обычные:(.*?)(?=Срочные:|Ссылка на записи:|$)', content, re.DOTALL)

    if urgent_match:
        sections['Срочные'] = urgent_match.group(1).strip()
    if regular_match:
        sections['Обычные'] = regular_match.group(1).strip()

    # Находим ссылку
    link_match = re.search(r'Ссылка на записи:\s*(.*)', content)
    link = link_match.group(1).strip() if link_match else ''

    # Обрабатываем блоки для каждой секции
    all_blocks = []

    for section_type, section_content in sections.items():
        # Разбиваем секцию на блоки (группы по 4 строки)
        lines = [line.strip() for line in section_content.split('\n') if line.strip()]

        i = 0
        while i < len(lines):
            if i + 3 < len(lines):  # Убедимся, что у нас есть 4 строки
                block = lines[i:i + 4]
                price = 120 if section_type == 'Срочные' else 75
                all_blocks.append((block, price))
                i += 4
            else:
                # Если осталось меньше 4 строк, пропускаем
                i += 1

    # Write the output to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')

        # Write the header
        csv_writer.writerow(['Fourth Line', 'Second Line', 'First Line', 'Date', 'Duration', 'Price', 'Link'])

        # Process each block and write to the CSV
        for block, price in all_blocks:
            if len(block) == 4:
                fourth_line = block[3]
                second_line = block[1]
                first_line = block[0]
                date = extract_date(block[2])
                duration = get_duration_minutes(block[1])
                csv_writer.writerow([fourth_line, second_line, first_line, date, duration, price, link])


# Example usage
input_file = 'input.txt'  # Replace with your input file name
output_file = 'output.csv'  # Replace with your desired output file name
process_text_file(input_file, output_file)