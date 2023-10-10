from datetime import date

import pytest

from src.api.repository import SqlAlchemyRepository
import src.db.models as models


class TestSqlAlchemyRepository:
    def test_insert_party_donation_valid(self, session):
        repository = SqlAlchemyRepository(session)
        party_donation = models.PartyDonation(
            id=1, amount=1000.0, date=date(2020, 1, 1), party_id=1
        )
        # Act
        repository.add(party_donation=party_donation)
        session.commit()
        # Assert
        assert session.query(models.PartyDonation).count() == 1
        # Cleanup
        session.delete(party_donation)
        session.commit()

    @pytest.mark.xfail(raises=Exception)
    def test_insert_party_donation_no_date_invalid(self, session):
        try:
            repository = SqlAlchemyRepository(session)
            # Act
            party_donation = models.PartyDonation(
                id=1,
                amount=1000.0,
            )
            repository.add(party_donation=party_donation)
            session.commit()

        except Exception:
            session.rollback()

    def test_get_party_donation(self, session):
        repository = SqlAlchemyRepository(session)
        party_donation = models.PartyDonation(
            id=2, amount=1000.0, date=date(2020, 1, 1), party_id=2
        )
        session.add(party_donation)
        session.commit()
        # Act and Assert
        assert repository.get("id", 2) == party_donation
        assert repository.get("party_id", 2) == party_donation
        session.delete(party_donation)
        session.commit()
