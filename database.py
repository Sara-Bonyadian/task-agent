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

# --- Add these: session dependency + init function ---

def get_db():
    """
    WHY a generator?
    - FastAPI dependencies can yield a resource. Code after `yield` runs
      as a `finally` block, guaranteeing the session closes even on errors.
    - This pattern prevents session leaks and keeps each request isolated.
    """
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    WHY a function (not at import)?
    - We want to control *when* tables are created (e.g., on app startup).
    - Avoids side effects during imports and makes tests cleaner.
    """
    from models import TaskDB  # local import to avoid circulars
    Base.metadata.create_all(bind=engine)