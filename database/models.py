from sqlalchemy import (
Column,
Integer,
String,
Text,
Float,
ForeignKey,
CheckConstraint
)

from sqlalchemy import relationship, declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship to game event
    game_events = relationship("GameEvent", back_populates="player")

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.name}')>"

class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(String, nullable=False)

    #Relationship to game_event
    game_events = relationship("GameEvent", back_populates="session")
    def __repr__(self):
        return f"<Session(session_id={self.session_id}, start_time= '{self.start_time}')>"


class GameEvent(Base):
    __tablename__ = "game_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    session_id = Column(Integer, ForeignKey('sessions.session_id'), nullable=False)
