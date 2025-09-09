from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL: tells SQLAlchemy how to connect
DATABASE_URL="postgresql+psycopg2://sarabonyadian@localhost:5432/taskdb"

# Create the engine (like a cable connecting Python ↔ Postgres)
engine=create_engine(DATABASE_URL)

# Session: the "conversation" we use for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: parent class for all tables
Base = declarative_base()