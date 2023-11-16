from datetime import date
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.connection import Base
from src.db.models.party import Party
from src.db.models.party_donation import PartyDonation
from src.db.models.party_style import PartyStyle
from src.db.models.party_donation_organization import PartyDonationOrganization


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

    # Cleanup
    for party_donation in party_donations:
        session.delete(party_donation)
    session.commit()


def get_postgres_url() -> str:
    """Get the postgres url from environment variables."""

    host = os.environ.get("TESTING_DATABASE_HOST", "localhost")
    port = os.environ.get("TESTING_DATABASE_PORT", 5432)
    user = os.environ.get("TESTING_DATABASE_USER", "postgres")
    password = os.environ.get("TESTING_DATABASE_PASSWORD", "password")
    db = os.environ.get("TESTING_DATABASE_NAME", "ftf_test_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


# Arrange
@pytest.fixture(scope="module")
def postgres_db():
    """Create a postgres database for testing."""
    postgres_url = get_postgres_url()
    engine = create_engine(postgres_url)
    Base.metadata.create_all(engine)
    return engine


# Arrange
@pytest.fixture
def postgres_session(postgres_db):
    """Create a postgres session for testing."""
    session = sessionmaker(bind=postgres_db)()
    yield session
    # Clean up
    session.rollback()
    session.close()


# Arrange
@pytest.fixture
def setup_sqlite_party_related_tables(session):
    """Create a postgres session with party related tables for testing."""
    # PartyStyle
    party_style_data = [
        (1, "CDU", "#000000", "#FFFFFF", "#000000"),
        (2, "SPD", "#000000", "#FFFFFF", "#000000"),
        (3, "FDP", "#000000", "#FFFFFF", "#000000"),
        (4, "AfD", "#000000", "#FFFFFF", "#000000"),
    ]
    party_styles = [
        PartyStyle(
            id=id,
            display_name=display_name,
            foreground_color=foreground_color,
            background_color=background_color,
            border_color=border_color,
        )
        for id, display_name, foreground_color, background_color, border_color in party_style_data
    ]
    session.add_all(party_styles)
    session.commit()

    # Party
    party_data = [
        (
            1,
            "party",
            "CDU",
            "https://www.abgeordnetenwatch.de/api/parties/1",
            "Christlich Demokratische Union Deutschlands",
            "CDU",
            1,
        ),
        (
            2,
            "party",
            "SPD",
            "https://www.abgeordnetenwatch.de/api/parties/2",
            "Sozialdemokratische Partei Deutschlands",
            "SPD",
            2,
        ),
        (
            3,
            "party",
            "FDP",
            "https://www.abgeordnetenwatch.de/api/parties/3",
            "Freie Demokratische Partei",
            "FDP",
            3,
        ),
        (
            4,
            "party",
            "AfD",
            "https://www.abgeordnetenwatch.de/api/parties/4",
            "Alternative für Deutschland",
            "AfD",
            4,
        ),
    ]
    parties = [
        Party(
            id=id,
            entity_type=entity_type,
            label=label,
            api_url=api_url,
            full_name=full_name,
            short_name=short_name,
            party_style_id=party_style_id,
        )
        for id, entity_type, label, api_url, full_name, short_name, party_style_id in party_data
    ]
    session.add_all(parties)
    session.commit()

    # PartyDonationOrganization
    party_donation_organization_data = [
        (1, "Stefan Quandt", "Seedammweg 55", "61352", "Bad Hamburg", False),
        (2, "Susanne Klatten", "Seedammweg 55", "61352", "Bad Hamburg", False),
        (3, "Friede Springer", "Axel-Springer-Str. 65", "10888", "Berlin", False),
        (4, "Friede Springer", "Axel-Springer-Str. 65", "10888", "Berlin", False),
    ]
    party_donation_organizations = [
        PartyDonationOrganization(
            id=id,
            donor_name=donor_name,
            donor_address=donor_address,
            donor_zip=donor_zip,
            donor_city=donor_city,
            donor_foreign=donor_foreign,
        )
        for id, donor_name, donor_address, donor_zip, donor_city, donor_foreign in party_donation_organization_data
    ]
    session.add_all(party_donation_organizations)
    session.commit()

    # PartyDonation
    party_donation_data = [
        (1, 1000.0, date(2020, 1, 1), 1, 1),
        (2, 1000.0, date(2021, 1, 1), 1, 2),
        (3, 1000.0, date(2022, 1, 1), 2, 3),
        (4, 1000.0, date(2023, 1, 1), 2, 4),
    ]
    party_donations = [
        PartyDonation(
            id=id,
            amount=amount,
            date=d,
            party_id=party_id,
            party_donation_organization_id=party_donation_organization_id,
        )
        for id, amount, d, party_id, party_donation_organization_id in party_donation_data
    ]
    session.add_all(party_donations)
    session.commit()

    yield session

    # Cleanup
    session.query(PartyDonation).delete()
    session.query(PartyDonationOrganization).delete()
    session.query(Party).delete()
    session.query(PartyStyle).delete()
    session.commit()
    session.close()


# Arrange
@pytest.fixture
def setup_postgres_party_related_tables(postgres_session):
    """Create a postgres session with party related tables for testing."""
    # PartyStyle
    party_style_data = [
        (1, "CDU", "#000000", "#FFFFFF", "#000000"),
        (2, "SPD", "#000000", "#FFFFFF", "#000000"),
        (3, "FDP", "#000000", "#FFFFFF", "#000000"),
        (4, "AfD", "#000000", "#FFFFFF", "#000000"),
    ]
    party_styles = [
        PartyStyle(
            id=id,
            display_name=display_name,
            foreground_color=foreground_color,
            background_color=background_color,
            border_color=border_color,
        )
        for id, display_name, foreground_color, background_color, border_color in party_style_data
    ]
    postgres_session.add_all(party_styles)
    postgres_session.commit()

    # Party
    party_data = [
        (
            1,
            "party",
            "CDU",
            "https://www.abgeordnetenwatch.de/api/parties/1",
            "Christlich Demokratische Union Deutschlands",
            "CDU",
            1,
        ),
        (
            2,
            "party",
            "SPD",
            "https://www.abgeordnetenwatch.de/api/parties/2",
            "Sozialdemokratische Partei Deutschlands",
            "SPD",
            2,
        ),
        (
            3,
            "party",
            "FDP",
            "https://www.abgeordnetenwatch.de/api/parties/3",
            "Freie Demokratische Partei",
            "FDP",
            3,
        ),
        (
            4,
            "party",
            "AfD",
            "https://www.abgeordnetenwatch.de/api/parties/4",
            "Alternative für Deutschland",
            "AfD",
            4,
        ),
    ]
    parties = [
        Party(
            id=id,
            entity_type=entity_type,
            label=label,
            api_url=api_url,
            full_name=full_name,
            short_name=short_name,
            party_style_id=party_style_id,
        )
        for id, entity_type, label, api_url, full_name, short_name, party_style_id in party_data
    ]
    postgres_session.add_all(parties)
    postgres_session.commit()

    # PartyDonationOrganization
    party_donation_organization_data = [
        (1, "Stefan Quandt", "Seedammweg 55", "61352", "Bad Hamburg", False),
        (2, "Susanne Klatten", "Seedammweg 55", "61352", "Bad Hamburg", False),
        (3, "Friede Springer", "Axel-Springer-Str. 65", "10888", "Berlin", False),
        (4, "Friede Springer", "Axel-Springer-Str. 65", "10888", "Berlin", False),
    ]
    party_donation_organizations = [
        PartyDonationOrganization(
            id=id,
            donor_name=donor_name,
            donor_address=donor_address,
            donor_zip=donor_zip,
            donor_city=donor_city,
            donor_foreign=donor_foreign,
        )
        for id, donor_name, donor_address, donor_zip, donor_city, donor_foreign in party_donation_organization_data
    ]
    postgres_session.add_all(party_donation_organizations)
    postgres_session.commit()

    # PartyDonation
    party_donation_data = [
        (1, 1000.0, date(2020, 1, 1), 1, 1),
        (2, 1000.0, date(2021, 1, 1), 1, 2),
        (3, 1000.0, date(2022, 1, 1), 2, 3),
        (4, 1000.0, date(2023, 1, 1), 2, 4),
    ]
    party_donations = [
        PartyDonation(
            id=id,
            amount=amount,
            date=d,
            party_id=party_id,
            party_donation_organization_id=party_donation_organization_id,
        )
        for id, amount, d, party_id, party_donation_organization_id in party_donation_data
    ]
    postgres_session.add_all(party_donations)
    postgres_session.commit()

    yield postgres_session

    # Cleanup
    postgres_session.query(PartyDonation).delete()
    postgres_session.query(PartyDonationOrganization).delete()
    postgres_session.query(Party).delete()
    postgres_session.query(PartyStyle).delete()
    postgres_session.commit()
    postgres_session.close()
