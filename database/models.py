from sqlalchemy import (
Column,
Integer,
String,
Float,
ForeignKey,
JSON,
CheckConstraint
)

from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    game_events = relationship("GameEvent", back_populates="player")

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.name}')>"

class Round(Base):

    """A round is a set of games each of which can have many events"""
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(String, nullable=False)
    # end_time = Column(String, nullable=False)

    # Relationship to game event
    games = relationship("Game", back_populates="round", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Round(id{self.id}, start_time {self.start_time})>"


class Game(Base):
    """Each round has 10 games. This table stores 1 row per game referencing which round it belongs to"""

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)
    game_index = Column(Integer, nullable=False)

    # Relationship back to round
    round = relationship("Round", back_populates="games")

    # Each game can have multiple game events
    game_events = relationship("GameEvent", back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game(id={self.id}, round_id={self.round_id}, game_index={self.game_index})>"


class GameEvent(Base):
    """Each row here represents an event in a single game, such as correct response etc"""
    __tablename__ = "game_events"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Link to player
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    # Link to game
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)


    #Link to round
    # round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)

    event_index = Column(Integer, nullable=False)
    n_back_value = Column(Integer, nullable=False)
    actual_number = Column(Integer, nullable=False)
    player_number_response = Column(Integer)
    number_response_status = Column(
        String, CheckConstraint("number_response_status IN ('correct', 'incorrect', 'missed')")
        )
    actual_position = Column(JSON, nullable=False)
    player_position_response =Column(JSON)
    position_response_status = Column(
        String, CheckConstraint("position_response_status IN ('correct', 'incorrect', 'missed')"))
    position_response_time = Column(Float)
    number_response_time = Column(Float)

    # Relationships
    player = relationship("Player", back_populates="game_events")
    game = relationship("Game", back_populates="game_events")

    def __repr__(self):
        return (f"<GameEvent("
                f"id={self.id}, "
                f"player_id{self.player_id},"
                f"game_id{self.game_id})>")
