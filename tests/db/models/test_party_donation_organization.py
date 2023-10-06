import pytest

from src.db.models.party_donation_organization import PartyDonationOrganization


class TestPartyDonationOrganization:
    def test_insert_party_donation_organization_valid(self, session):
        # Act
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
        session.delete(party_donation_organization)

    @pytest.mark.xfail(raises=Exception)
    def test_insert_party_donation_organization_no_donor_name_invalid(self, session):
        try:
            # Act
            party_donation_organization = PartyDonationOrganization(
                id=1,
                donor_address="Test Address",
                donor_zip="12345",
                donor_city="Test City",
                donor_foreign=True,
            )
            session.add(party_donation_organization)
            session.commit()
        except Exception:
            session.rollback()
