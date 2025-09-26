from pydub import AudioSegment
import os


# Function to convert m4a to mp3
def convert_m4a_to_mp3(input_file):
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"The file {input_file} does not exist.")
        return

    # Load the .m4a file
    sound = AudioSegment.from_file(input_file, format="m4a")

    # Define the output file name
    output_file = input_file.rsplit('.', 1)[0] + '.mp3'  # Change extension to .mp3

    # Export as .mp3
    sound.export(output_file, format="mp3")

    print(f"Converted {input_file} to {output_file}")


# Specify the input .m4a file name
input_file = '07.15_1_zoom_12.00(01.55).webm'
convert_m4a_to_mp3(input_file)