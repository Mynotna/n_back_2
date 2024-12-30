import sqlite3
import json
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import SessionLocal
from .models import Player, Session as SessionModel, GameEvent


class DataManager:
    def __init__(self):
        self.session: Session = SessionLocal()


    def add_player(self, name: str) -> Player:
        """Add a player with a unique name or select an existing one"""
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


    def get_player_by_name(self, name: str) -> Player:
        return self.session.query(Player).filter_by(name=name).first()

    def start_new_session(self) -> SessionModel:
        """Create a new session in the db"""
        session_obj = SessionModel(start_time=datetime.now().isoformat())
        self.session.add(session_obj)
        self.session.commit()
        self.session.refresh(session_obj)
        return session_obj

    def save_game_event(
            self,
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
    ) -> GameEvent:

        """Save a new game event to db"""
        event = GameEvent(
            player_id= player_id,
            session_id= session_id,
            game_id= game_id,
            event_index= event_index,
            n_back_value= n_back_value,
            actual_number= actual_number,
            player_number_response= player_number_response,
            number_response_status= number_response_status,
            actual_position= actual_position, # convert tuples to json strings
            player_position_response= player_position_response
                if player_position_response else None,
            position_response_status= position_response_status,
            position_response_time= position_response_time,
            number_response_time= number_response_time
        )

        self.session.add(event)
        self.session.commit()
        self.session.refresh()
        return event

    def close(self):
        self.session.close()

if __name__ == "__main__":
    print("Hello")