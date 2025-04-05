from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'scheduler')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'scheduler')}@"
    f"{os.getenv('POSTGRES_HOST', 'db')}/"
    f"{os.getenv('POSTGRES_DB', 'scheduler')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
