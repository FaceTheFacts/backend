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
    username=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWORD"],
    host=os.environ["DATABASE_HOST"],
    database=os.environ["DATABASE_NAME"],
)

engine = create_engine(connection_uri, pool_size=50, max_overflow=50)
Session = sessionmaker(bind=engine)
Base = declarative_base()
