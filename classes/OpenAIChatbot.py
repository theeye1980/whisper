import json
import requests
import datetime
import sqlite3
from classes.config import SECRET_KEY

class OpenAIChatbot:
    def __init__(self):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            'Authorization': SECRET_KEY,
            'Content-Type': 'application/json'
        }
        # connect to SQLite database
        conn = sqlite3.connect('requests.db')

        # check if table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='log'")
        table_exists = cursor.fetchone() is not None

        # create table if it doesn't exist
        if not table_exists:
            cursor.execute('''CREATE TABLE log
                                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       timestamp DATETIME,
                                       ask TEXT,
                                       answer TEXT)''')
            conn.commit()
            print("Table created successfully")
    def get_response(self, promt, model,temperature=0.7):
        payload = json.dumps({
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": promt
                }
            ],
            "temperature": temperature
        })
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        return response.text

    def write_to_file(self, promt, content):
        with open('content.txt', 'a',  encoding='utf-8') as file:
            file.write('Вопрос:\n' + promt + '\n' + 'Ответ:\n' + content + '_________' + '\n\n')

    def get_last_entries(self, count):
        # connect to SQLite database
        conn = sqlite3.connect('requests.db')
        # retrieve all entries from table
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM log ORDER BY id DESC limit {count}")
        entries = cursor.fetchall()
        # close connection
        conn.close()
        return entries
