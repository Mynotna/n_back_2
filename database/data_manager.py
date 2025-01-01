from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import SessionLocal
from .models import (
    Player,
    Round,
    Game,
    GameEvent
)


class DataManager:
    def __init__(self):
        self.session: Session = SessionLocal() # This is the ORM obj

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

    def start_new_round(self) -> Round:
        """Create a new round in the db (equivalent to 10 games)"""
        round_obj = Round(start_time=datetime.now().isoformat())
        self.session.add(round_obj)
        self.session.commit()
        self.session.refresh(round_obj)
        return round_obj

    def create_game(self, round_id: int, game_index: int, ) -> Game:
        """
        Create a new game within a round. There are 10 games per round
        :param round_id:
        :param game_index:
        :return: Game
        """
        new_game = Game(round_id=round_id, game_index=game_index)
        self.session.add(new_game)
        self.session.commit()
        self.session.refresh(new_game)
        return new_game

    def save_game_event(
            self,
            player_id,
            round_id,
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

        """Save a new event in single game event to db"""
        event = GameEvent(
            player_id=player_id,
            game_id=game_id,
            event_index=event_index,
            n_back_value=n_back_value,
            actual_number=actual_number,
            player_number_response=player_number_response,
            number_response_status=number_response_status,
            actual_position=actual_position,
            player_position_response=player_position_response
            if player_position_response else None,
            position_response_status=position_response_status,
            position_response_time=position_response_time,
            number_response_time=number_response_time
        )

        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def close(self):
        self.session.close()


if __name__ == "__main__":
    print("Hello")
