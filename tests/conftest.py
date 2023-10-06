from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.connection import Base
from src.db.models.party_donation import PartyDonation


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


@pytest.fixture
def setup_party_donations(session):
    party_donation_data = [
        (1, 1000.0, date(2020, 1, 1), 1),
        (2, 1000.0, date(2021, 1, 1), 1),
        (3, 1000.0, date(2022, 1, 1), 2),
        (4, 1000.0, date(2023, 1, 1), 3),
    ]

    party_donations = [
        PartyDonation(id=id, amount=amount, date=d, party_id=party_id)
        for id, amount, d, party_id in party_donation_data
    ]

    session.add_all(party_donations)
    session.commit()

    yield session

    # Clean Up
    for party_donation in party_donations:
        session.delete(party_donation)
    session.commit()
