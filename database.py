from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Location of database file
DATABASE_URL = "sqlite:///./database.db"

# create_engine creates a new engine instance that connects to the database specified in DATABASE_URL.
# connect_args is used to make sure that SQLite works well with threads.
engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})

# sessionmaker creates a class SessionLocal that can be used to create a database session.
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()
