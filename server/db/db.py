import os
from pathlib import Path 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import inspect


BASE_DIR = Path(__file__).resolve().parent.parent  # server/ directory
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Read db url from .env file
DATABASE_URL = os.getenv("DATABASE_URL", '')

# check_same_thread: False allows multiple threads to use the db connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo='debug')

SessionLocal = sessionmaker(autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables in database: {tables}")
print(DATABASE_URL)