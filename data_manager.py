import sqlite3
from datetime import datetime

class DataManager:
    def __init__(self, db_name= 'game_data.db')
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.session_id = None

    def create_tables(self):
        # Create tables to store game data
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS session(
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time Text
                )
            ''')

        self.cursor.execute('''
            CREAT TABLE IF NOT EXISTS responses(
            id INTERGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            timestamp Text,
            response_type TEXT,
            is_correct INTEGER,
            missed INTEGER,
            FOREIGN KEY(session_id) REFERENCES sessions(session_id)
                )
            ''')
        self.conn.commit()


    def start_new_session(self):
        start_time = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO sessions (start_time) VALUES (?)
            ''', (start_time,))
        self.session_id = self.cursor.lastrowid
        self.conn.commit()


    def save_generated_data(self, timestamp, number, position):
        self.cursor.execute('''
        INSERT INTO generated_data (session_id, timestamp, number, position_x, position_y)
        VALUES (?, ?, ?, ?, ?)
        '''), (self.session_id, timestamp, number, position[0], position[1])
        self.conn.commit()


    def save_response(self, timestamp, response_type, is_correct, missed):
        self.cursor.execute('''
        INSERT INTO responses(session_id, timestamp, response_type, is_correct, missed)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.session_id, timestamp, response_type, is_correct, missed ))
        self.conn.commit()

    def close(self):
        self.conn.close()