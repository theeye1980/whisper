import re
import os

# Настройки
low_density_value = 10 #Число знаков в секунду. Если ниже, то считаем это участком с низкой плотностью текста
ld_in_row = 4 #количество участков подряд, при которых надо включать информацию в отчет

report_filename = 'report.txt'
reports_directory = 'reports'


# Check if the directory exists
if not os.path.exists(reports_directory):
    # Create the directory
    os.makedirs(reports_directory)
    print(f'Directory "{reports_directory}" created.')
else:
    print(f'Directory "{reports_directory}" already exists.')


def analyze_timestamps(file_path):
    with open(file_path, 'r', encoding='cp1251') as file:
        content = file.read()

    # Regular expression to match timestamps in the format HH:MM:SS:
    timestamp_pattern = r'(\d{2}:\d{2}:\d{2}):'
    timestamps = re.findall(timestamp_pattern, content)

    # Initialize a list to hold the results
    results = []
    low_density = []

    # Find all matches for timestamps and their following text
    matches = re.finditer(r'(\d{2}:\d{2}:\d{2}):\s*(.*?)(?=\d{2}:\d{2}:\d{2}:|$)', content, re.DOTALL)

    previous_time = None
    low_density_count = 0
    low_density_start_time = None  # To track the start of low density sequences
    low_density_end_time = None  # To track the end of low density sequences

    for match in matches:
        current_time = match.group(1)
        text_segment = match.group(2).strip()

        # Calculate the length of the text segment
        text_length = len(text_segment)

        # Convert timestamps to seconds for density calculation
        if previous_time is not None:
            start_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(previous_time.split(':'))))
            end_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(current_time.split(':'))))
            duration = end_seconds - start_seconds

            # Calculate density (length divided by duration)
            density = text_length / duration if duration > 0 else 0

            # Append the result as a tuple (timestamp, density)
            results.append((previous_time, density))

            # Check for low density
            if density < low_density_value:
                low_density_count += 1
                # Capture the start time of the low density sequence
                if low_density_count == 1:
                    low_density_start_time = previous_time
                # Update the end time of the low density sequence
                low_density_end_time = current_time
            else:
                # If we had a sequence of low densities, check if it was more than 4
                if low_density_count > ld_in_row:
                    low_density.append((low_density_start_time, low_density_end_time))  # Add the first and last timestamps of the sequence
                low_density_count = 0  # Reset the count if density is not low
                low_density_start_time = None  # Reset the start time
                low_density_end_time = None  # Reset the end time

        previous_time = current_time

    # Final check in case the last sequence was low density
    if low_density_count > ld_in_row:
        low_density.append((low_density_start_time, low_density_end_time))

    return results, low_density

#scan the folder for txt files
# Get the current directory
current_directory = os.getcwd()

# List to hold the names of .txt files
txt_files = []

# Loop through the files in the current directory
for file in os.listdir(current_directory):
    if file.endswith('.txt'):
        txt_files.append(file)

# Loop through the txt files
for file in txt_files:
    timestamp_densities, low_density = analyze_timestamps(file)

    # Split the filename into name and extension
    file_name, file_extension = os.path.splitext(file)

    # Create the new filename with the suffix '_report'
    new_filename = f"{reports_directory}/{file_name}_report{file_extension}"
    # Open the file in write mode

    with open(new_filename, 'w') as report_file:
        # Write the header

        # Print low density timestamps
        if low_density:  # Check if low_density has elements
            for start_ts, end_ts in low_density:
                report_file.write(f'\n Начало подозрительного участка: {start_ts}, Конец: {end_ts}')
        else:
            report_file.write('\n Нет участков с низкой плотностью текста.')

        # Write each timestamp and density to the file
        for timestamp, density in timestamp_densities:
            report_file.write(f'\n Метка: {timestamp}, Плотность: {density:.2f}')

    # Print low density timestamps
    if low_density:  # Check if low_density has elements

        print(f"\n {file}: Участки с низкой плотностью текста (Начало, Конец):")
        for start_ts, end_ts in low_density:
            print(f' \n Начало подозрительного участка: {start_ts}, Конец: {end_ts}')

    else:
        print(f'\n {file}: Нет участков с низкой плотностью текста.')
# # Example usage
# file_path = '10.17_2_4Floor_10.00(06.35)_.txt'  # Replace with your actual file path
# timestamp_densities, low_density = analyze_timestamps(file_path)

# # Print the results
# print("Timestamp Densities:")
# for timestamp, density in timestamp_densities:
#     print(f'Timestamp: {timestamp}, Density: {density:.2f}')

