import sqlite3
import json
from datetime import datetime

class DataManager:
    def __init__(self, db_name='n_back_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.session_id = None

    def create_tables(self):
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT NOT NULL
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    game_id INTEGER NOT NULL,
                    event_index INTEGER NOT NULL,
                    n_back_value INTEGER NOT NULL,
                    actual_value INTEGER NOT NULL,
                    player_number_response INTEGER,
                    number_response_status TEXT CHECK(number_response_status IN("correct", "incorrect", "missed")),
                    actual_position TEXT NOT NULL,
                    player_position_response TEXT,
                    position_response_status TEXT CHECK(position_response_status IN("correct", "incorrect", "missed")),
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
                )
            ''')
            self.conn.commit()

    def start_new_session(self):
        start_time = datetime.now().isoformat()
        self.cursor.execute("INSERT INTO sessions (start_time) VALUES (?)", (start_time,))
        self.session_id = self.cursor.lastrowid
        self.conn.commit()


    def save_game_event(self, game_id, event_index, n_back_value, actual_number,
                        player_number_response, number_status, actual_position, player_position_response,
                        position_status):
        self.cursor.execute('''
        INSERT INTO game_events (
        session_id, game_id, event_index, n_back_value, actual_number,
        player_number_response, number_status, actual_position, player_position_response,
        position_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',(
            self.session_id, game_id, event_index, n_back_value,
            actual_number, player_number_response, number_status,
            json.dumps(actual_position), json.dumps(player_position_response), position_status
        ))
        self.conn.commit()


    def close(self):
        self.conn.close()


if __name__ == "__main__":
    dm = DataManager()
    print("game_data.db tables created successfully")
