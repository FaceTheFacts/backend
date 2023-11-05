from datetime import date

import pytest

from src.db.models.party_donation import PartyDonation


class TestPartyDonation:
    def test_insert_party_donation_valid(self, session, setup_party_donations):
        result = session.query(PartyDonation).filter(PartyDonation.id == 1).first()
        # Assert
        assert result.date == date(2020, 1, 1)

    @pytest.mark.xfail(raises=Exception)
    def test_insert_party_donation_no_date_invalid(self, session):
        try:
            # Act
            party_donation = PartyDonation(
                id=1,
                amount=1000.0,
            )
            session.add(party_donation)
            session.commit()
        except Exception:
            session.rollback()
