import sqlite3
import json
from datetime import datetime
from tkinter.font import names

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from .database import SessionLocal
from .models import Player, Session as SessionModel, GameEvent



class DataManager:
    def __init__(self):
        self.session: Session = SessionLocal()


    def add_player(self):
        """Add a player with a unique name or select an existing one"""(
        try:
            new_player = Player(name=name)
            self.session.add(new_player)
            self.session.commit()
            self.session.refresh(new_player)
            return new_player
        except IntegrityError:
            self.session.rollback()
            # If name already taken, fetch the existing player
            return self.get_player_by_name(name)


    def get_player_by_name(self):
        return self.session.query(Player).filter_by(name=names).first()


    def start_new_session(self):
        """Create a new session in the db"""
        session_obj = SessionModel(start_time=datetime.now().isoformat())
        self.session.add(session_obj)
        self.session.commit()
        self.session.refresh(session_obj)
        return session_obj




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
        position_response_status,
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
