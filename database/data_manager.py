import sqlite3
import json
from datetime import datetime


class DataManager:
    def __init__(self, db_name='n_back_scores.db'):
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
                    player_id TEXT NOT NULL,
                    session_id INTEGER NOT NULL,
                    game_id INTEGER NOT NULL,
                    event_index INTEGER NOT NULL,
                    n_back_value INTEGER NOT NULL,
                    actual_number INTEGER NOT NULL,
                    player_number_response INTEGER,
                    number_response_status TEXT CHECK(number_response_status IN("correct", "incorrect", "missed")),
                    actual_position TEXT NOT NULL,
                    player_position_response TEXT,
                    position_response_status TEXT CHECK(position_response_status IN("correct", "incorrect", "missed")),
                    position_response_time REAL NOT NULL,
                    number_response_time REAL NOT NULL,
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
                )
            ''')
            self.conn.commit()

    def start_new_session(self):
        start_time = datetime.now().isoformat()
        self.cursor.execute("INSERT INTO sessions (start_time) VALUES (?)", (start_time,))
        self.session_id = self.cursor.lastrowid
        self.conn.commit()


    def save_game_event(self,
                        player_id,
                        session_id,
                        game_id,
                        event_index,
                        n_back_value,
                        actual_number,
                        player_number_response,
                        number_response_status,
                        actual_position,
                        player_position_response,
                        position_response_status,
                        position_response_time,
                        number_response_time
        ):

        self.cursor.execute('''
        INSERT INTO game_events (
        player_id,
        session_id, 
        game_id, 
        event_index, 
        n_back_value, 
        actual_number,
        player_number_response, 
        number_response_status, 
        actual_position, 
        player_position_response,
        position_response_status
        position_response_time,
        number_response_time
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            player_id,
            self.session_id,
            game_id,
            event_index,
            n_back_value,
            actual_number,
            player_number_response,
            number_response_status,
            json.dumps(actual_position),
            json.dumps(player_position_response),
            position_response_status,
            position_response_time,
            number_response_time
        ))
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    dm = DataManager()
    dm.start_new_session()
    dm.save_game_event(
        player_id="dwindler_987",
        session_id=dm.session_id,
        game_id=1,
        event_index=0,
        n_back_value=2,
        actual_number=5,
        player_number_response=1,
        number_response_status="correct",
        actual_position=(100, 200),
        player_position_response=None,
        position_response_status="missed",
        position_response_time= 200,
        number_response_time= 200
    )
print("Game event saved successfully.")
