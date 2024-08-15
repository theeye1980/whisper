from classes.bd import bdSQLite
from classes.TextFileReader import TextFileReader
import numpy as np

#Задаем переменные
segments = 14


db = bdSQLite()


def find_nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def get_nearest_indexes(start_chunk_times, unique_start_times):
    nearest_indexes = []

    for time in unique_start_times:
            nearest_idx = find_nearest_index(start_chunk_times, time)
            nearest_indexes.append(nearest_idx)

    return nearest_indexes


# Выдернем все записи по спикерам и временным меткам
speakers, start_speak_times, unique_start_times = db.get_speaker_start_time_arrays()

# ВЫдернем записи с кусочками текстов
chunks, start_chunk_times = db.get_chunk_start_time_arrays()


nearest_indexes = get_nearest_indexes(start_chunk_times, unique_start_times)



#Запускаем процесс сборки текста
txt = TextFileReader("")
new_timeline_need = True
segment_count=segments
all_text = '' # Задаем переменную для альтернативного текста
elements = len(chunks)
for i in range(0,elements):
     chunk = chunks[i]
     start_time = start_chunk_times[i]

     start_str = txt.ts_format(start_time)
     if segment_count > segments - 1:
         out = '\n' + start_str + ': ' + chunk
         segment_count = 0
     else:
         out = chunk

     if segment_count > segments - 8 and segment_count > 3:
         if new_timeline_need:
             print('hi')
             out = '\n' + start_str + ': ' + chunk
             segment_count = 0

     # Вставляем проверку на совпадение с метками смены спикера и вставляем метку



     if i in nearest_indexes:
        out = '\n\n' + 'SPEAKER_CHANGE' + '\n' + out
     else:
         print(f"{start_time} is not in the list.")

     # self.save_string_to_file(self.log_file, out)
     all_text = all_text + " " + out

     # Проверем, нужно ли в следующий раз указывать тайминг при записи
     new_timeline_need = txt.check_string(chunk)
     segment_count = segment_count + 1

txt.save_string_to_file("new.txt", all_text)
print ("рш")
