import pytest
from sqlalchemy import text

from src.db.models.party_donation_organization import PartyDonationOrganization


def insert_party_donation_organization(session):
    # Arrange
    party_donation_organization = PartyDonationOrganization(
        id=1,
        donor_name="Test Donor",
        donor_address="Test Address",
        donor_zip="12345",
        donor_city="Test City",
        donor_foreign=True,
    )
    session.add(party_donation_organization)
    session.commit()


def delete_party_donation_organization(session):
    # Cleanup
    session.execute(text("DELETE FROM party_donation_organization"))
    session.commit()


class TestPartyDonationOrganization:
    def test_insert_party_donation_organization_valid(self, session):
        # Arrange
        insert_party_donation_organization(session)
        result = (
            session.query(PartyDonationOrganization)
            .filter(PartyDonationOrganization.id == 1)
            .first()
        )
        # Assert
        assert result.donor_name == "Test Donor"
        assert result.donor_address == "Test Address"
        assert result.donor_zip == "12345"
        assert result.donor_city == "Test City"
        assert result.donor_foreign == True

        # Cleanup
        delete_party_donation_organization(session)

    @pytest.mark.xfail(raises=Exception)
    def test_insert_party_donation_organization_no_donor_name_invalid(self, session):
        try:
            # Arrange
            insert_party_donation_organization(session)
        except Exception:
            session.rollback()
        # Cleanup
        delete_party_donation_organization(session)
