import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.connection import Base


# Arrange
@pytest.fixture(scope="module")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


# Arrange
@pytest.fixture
def session(in_memory_db):
    session = sessionmaker(bind=in_memory_db)()
    yield session
    # Clean up
    session.rollback()
    session.close()
