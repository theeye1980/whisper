import ffmpeg

input_file = '08.20_1_vzd_13.00(00.52).webm'
output_file = '08.20_1_vzd_13.00(00.52).mp3'

(
    ffmpeg
    .input(input_file)
    .output(output_file, format='mp3', acodec='libmp3lame')
    .run()
)