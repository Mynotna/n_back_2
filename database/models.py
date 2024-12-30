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

    game_events = relationship("GameEvent", back_populates= "player")

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.name}')>"

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(String, nullable=False)

    # Relationship to game event
    game_events = relationship("GameEvent", back_populates="session")

    def __repr__(self):
        return f"<Session(session_id{self.id}, start_time'{self.start_time}')>"


class GameEvent(Base):
    __tablename__ = "game_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Foreign key connections
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)

    game_id = Column(Integer, nullable=False)
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
    session = relationship("Session", back_populates="game_events")

    def __repr__(self):
        return (f"<game_event("
                f"id={self.id}, "
                f"player_id{self.player_id},"
                f"session_id{self.session_id})>")
