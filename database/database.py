from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "database/n_back_data.db"

#Create the engine
engine = create_engine(DATABASE_URL, echo=False)

#Create tables if they don't exist
Base.metadata.create_all(engine)

#Create a session factory
SessionLocal = sessionmaker(bind=engine)
