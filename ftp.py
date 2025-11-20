
from ftplib import FTP
from config import ftp_path,ftp_host,ftp_user_name, ftp_password
from classes.TextFileReader import TextFileReader

txt = TextFileReader("")
file_paths = txt.list_projects_files(".")

print  (file_paths)

# Подключаемся к FTP
ftp = FTP(ftp_host)
ftp.login(user=ftp_user_name, passwd=ftp_password)
ftp.cwd(ftp_path)  # переходим в нужную директорию на FTP

for file_path in file_paths:
    with open(file_path, 'rb') as f:
        # Имя файла на FTP будет таким же, как локальное имя
        filename = file_path.split('/')[-1]  # или os.path.basename(file_path)
        print(f"Загружаем файл {filename} на FTP...")
        print(f" путь https://podvi.ru/n8n/{filename}")
        ftp.storbinary(f'STOR {filename}', f)

ftp.quit()
print("Все файлы загружены.")