# std
import os
from dotenv import load_dotenv

# third-party
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

connection_uri = sa.engine.URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    database=os.getenv("DATABASE_NAME"),
)

engine = create_engine(connection_uri)
Session = sessionmaker(bind=engine)
Base = declarative_base()
