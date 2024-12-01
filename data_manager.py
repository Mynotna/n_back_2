import sqlite3
from datetime import datetime

class DataManager:
    def __init__(self, db_name='game_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.session_id = None

    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    timestamp TEXT,
                    response_type TEXT,
                    is_correct INTEGER,
                    missed INTEGER,
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS generated_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    timestamp TEXT,
                    number INTEGER,
                    position_x REAL,
                    position_y REAL,
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
                )
            ''')
            self.conn.commit()
            print("Tables created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def start_new_session(self):
        start_time = datetime.now().isoformat()
        try:
            self.cursor.execute('''
                INSERT INTO sessions (start_time) VALUES (?)
            ''', (start_time,))
            self.session_id = self.cursor.lastrowid
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error starting new session: {e}")

    def save_generated_data(self, timestamp, number, position):
        try:
            self.cursor.execute('''
                INSERT INTO generated_data (session_id, timestamp, number, position_x, position_y)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.session_id, timestamp, number, position[0], position[1]))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving generated data: {e}")

    def save_response(self, timestamp, response_type, is_correct, missed):
        try:
            self.cursor.execute('''
                INSERT INTO responses (session_id, timestamp, response_type, is_correct, missed)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.session_id, timestamp, response_type, is_correct, missed))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving response: {e}")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    dm = DataManager()
    print("game_data.db tables created successfully")
