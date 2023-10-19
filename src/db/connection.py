# std
import os
from dotenv import load_dotenv

# third-party
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

database_connections = {
    "testing": {
        "database_user": os.environ["TESTING_DATABASE_USER"],
        "database_password": os.environ["TESTING_DATABASE_PASSWORD"],
        "database_host": os.environ["TESTING_DATABASE_HOST"],
        "database_name": os.environ["TESTING_DATABASE_NAME"],
    },
    "production": {
        "database_user": os.environ["DATABASE_USER"],
        "database_password": os.environ["DATABASE_PASSWORD"],
        "database_host": os.environ["DATABASE_HOST"],
        "database_name": os.environ["DATABASE_NAME"],
    },
}

current_env = os.environ.get("DB_ENV", "production")
connection_params = database_connections.get(current_env)

if connection_params:
    connection_uri = sa.engine.URL.create(
        "postgresql+psycopg2",
        username=connection_params["database_user"],
        password=connection_params["database_password"],
        host=connection_params["database_host"],
        database=connection_params["database_name"],
    )

    engine = create_engine(connection_uri, pool_size=50, max_overflow=50)
    Session = sessionmaker(bind=engine)
    Base = declarative_base()
else:
    # Handle the case where the some_env value is not recognized
    raise ValueError(f"Unknown environment: {current_env}")
