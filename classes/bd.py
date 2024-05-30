import datetime
import sqlite3
import pandas as pd

class bdSQLite:
    def __init__(self):
        self.bd = 'requests.db'
    def insert_request(self, ask, answer):
        # connect to SQLite database
        conn = sqlite3.connect(self.bd)

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

        timestamp = datetime.datetime.now()
        # insert request into table
        cursor.execute("INSERT INTO log (timestamp, ask, answer) VALUES (?, ?, ?)", (timestamp, ask, answer))
        conn.commit()
        print("Request inserted successfully")

        # close connection
        conn.close()

    def insert_speaker_data(self, audiofolders_id, speaker, start_time): # добавление информации по спикеру
        # Connect to the SQLite database
        conn = sqlite3.connect(self.bd)
        cursor = conn.cursor()

        # Insert data into the speakers table
        cursor.execute("INSERT INTO speakers (audiofolders_id, speaker, start_time) VALUES (?, ?, ?)",
                       (audiofolders_id, speaker, start_time))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def insert_text_autotrans_data(self, audiofolders_id, chunk, start_time):
        conn = sqlite3.connect(self.bd)  # Connect to your SQLite database
        cursor = conn.cursor()

        # Data to be inserted
        data = (audiofolders_id, chunk, start_time)

        # SQL query to insert data into the table
        cursor.execute('''
            INSERT INTO text_autotrans (audiofolders_id, chunk, start_time)
            VALUES (?, ?, ?)
        ''', data)

        conn.commit()  # Commit the changes
        conn.close()  # Close the connection

    def get_speaker_start_time_arrays(self):
        conn = sqlite3.connect(self.bd)  # Connect to your SQLite database
        cursor = conn.cursor()

        # Retrieve data from the speakers table
        cursor.execute('SELECT speaker, start_time FROM speakers')
        rows = cursor.fetchall()

        # Extract speaker and start_time data into separate arrays
        speakers = [row[0] for row in rows]
        start_times = [row[1] for row in rows]
        unique_start_times = []
        prev_speaker = None

        for speaker, start_time in zip(speakers, start_times):
            if speaker != prev_speaker:
                unique_start_times.append(start_time)

            prev_speaker = speaker

        conn.close()  # Close the connection

        return speakers, start_times, unique_start_times

    def get_chunk_start_time_arrays(self):
        conn = sqlite3.connect(self.bd)  # Connect to your SQLite database
        cursor = conn.cursor()

        # Retrieve data from the text_autotrans table
        cursor.execute('SELECT chunk, start_time FROM text_autotrans')
        rows = cursor.fetchall()

        # Extract chunk and start_time data into separate arrays
        chunks = [row[0] for row in rows]
        start_times = [row[1] for row in rows]

        conn.close()  # Close the connection

        return chunks, start_times
    def export(self, table):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.bd)  # Replace 'your_database.db' with the path to your SQLite database file

        # Query to select all data from the 'log' table
        query = f"SELECT * FROM {table}"

        # Load data from SQLite into a pandas DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the database connection
        conn.close()

        # Export the data to an Excel file
        excel_file = f'{table}_data.xlsx'  # Name of the Excel file to be created
        df.to_excel(excel_file, index=False)

        print("Data exported to Excel successfully.")