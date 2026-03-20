import csv
import re
import os
import requests
from datetime import datetime
from config import GOOGLE_DOCS_SHEET, GOOGLE_SHEET_WEBAPP_URL


def extract_date(line):
    match = re.search(r'\b\d{2}\.\d{2}\.\d{4}\b', line)
    return match.group(0) if match else ''


def get_duration_minutes(filename):
    match = re.search(r'\((\d{2})\.(\d{2})\)', filename)
    if not match:
        raise ValueError("Длительность в нужном формате не найдена в имени файла")
    hours = int(match.group(1))
    minutes = int(match.group(2))
    return hours * 60 + minutes


def append_to_google_sheet(row):
    try:
        requests.post(GOOGLE_SHEET_WEBAPP_URL, json={"row": row}, timeout=10)
    except Exception as e:
        print(f"Ошибка отправки в Google Sheet: {e}")


def process_text_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()

    sections = {}

    urgent_match = re.search(r'Срочные:(.*?)(?=Обычные:|Ссылка на записи:|$)', content, re.DOTALL)
    regular_match = re.search(r'Обычные:(.*?)(?=Срочные:|Ссылка на записи:|$)', content, re.DOTALL)

    if urgent_match:
        sections['Срочные'] = urgent_match.group(1).strip()
    if regular_match:
        sections['Обычные'] = regular_match.group(1).strip()

    link_match = re.search(r'Ссылка на записи:\s*(.*)', content)
    link = link_match.group(1).strip() if link_match else ''

    all_blocks = []

    for section_type, section_content in sections.items():
        lines = [line.strip() for line in section_content.split('\n') if line.strip()]

        i = 0
        while i < len(lines):
            if i + 3 < len(lines):
                block = lines[i:i + 4]
                price = 120 if section_type == 'Срочные' else 75
                all_blocks.append((block, price))
                i += 4
            else:
                i += 1

    today_date = datetime.now().strftime('%d.%m.%Y')
    write_header = not os.path.exists(output_file) or os.path.getsize(output_file) == 0

    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')

        if write_header:
            csv_writer.writerow(
                ['Today', 'Fourth Line', 'Second Line', 'First Line', 'Date', 'Duration', 'Price', 'Link'])

        for block, price in all_blocks:
            if len(block) == 4:
                fourth_line = block[3]
                second_line = block[1]
                first_line = block[0]
                date = extract_date(block[2])
                try:
                    duration = get_duration_minutes(block[1])
                except ValueError:
                    duration = 0

                row = [today_date, fourth_line, second_line, first_line, date, duration, price, link]
                csv_writer.writerow(row)
                append_to_google_sheet(row)


input_file = 'input.txt'
output_file = 'output.csv'
process_text_file(input_file, output_file)