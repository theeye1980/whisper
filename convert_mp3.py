from pydub import AudioSegment
import os
from config import input_folder

input_format = "mp4"
# input_format = "wav"
output_format = "mp3"
# Function to convert m4a to mp3
def convert_m4a_to_mp3(input_file):
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"The file {input_file} does not exist.")
        return

    # Load the .m4a file
    sound = AudioSegment.from_file(input_file, format=input_format)

    # Define the output file name
    output_file = input_file.rsplit('.', 1)[0] + '.' + output_format  # Change extension to .mp3

    # Export as .mp3
    sound.export(output_file, format=output_format)

    print(f"Converted {input_file} to {output_file}")


# Specify the input .m4a file name
# input_file = '07.15_1_zoom_12.00(01.55).webm'
# convert_m4a_to_mp3(input_file)

# Get audio files from the folder
file_list = [file_named for file_named in os.listdir(input_folder) if file_named.endswith("." + input_format)]

for file_name in file_list:
    file_path = os.path.join(input_folder, file_name)
    print (file_path)
    convert_m4a_to_mp3(file_path)