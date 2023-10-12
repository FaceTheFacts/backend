from datetime import date

import pytest
from sqlalchemy import text

from src.api.repository import SqlAlchemyFactory
import src.db.models as models


class TestSqlAlchemyRepository:
    # add
    def test_repository_can_save_a_party_donation(self, session):
        factory = SqlAlchemyFactory(session)
        repo = factory.create_party_donation_repository()
        party_donation = models.PartyDonation(
            id=1, amount=1000.0, date=date(2020, 1, 1), party_id=1
        )
        # Act
        repo.add(party_donation)
        session.commit()
        rows = session.execute(
            text("SELECT * FROM party_donation WHERE id = :id"), {"id": 1}
        )
        # Assert
        assert list(rows) == [(1, 1, 1000.0, "2020-01-01", None)]
        # Cleanup
        session.execute(text("DELETE FROM party_donation WHERE id = :id"), {"id": 1})
        session.commit()

    # add
    @pytest.mark.xfail(raises=Exception)
    def test_repository_cannot_save_a_party_donation_no_date(self, session):
        try:
            factory = SqlAlchemyFactory(session)
            repo = factory.create_party_donation_repository()
            # Act
            party_donation = models.PartyDonation(
                id=1,
                amount=1000.0,
            )
            repo.add(party_donation)
            session.commit()

        except Exception:
            session.rollback()

    def insert_party_donation(self, session):
        session.execute(
            text(
                "INSERT INTO party_donation (id, amount, date, party_id) "
                "VALUES (:id, :amount, :date, :party_id)"
            ),
            {"id": 2, "amount": 1000.0, "date": date(2020, 1, 1), "party_id": 1},
        )
        [[party_donation_id]] = session.execute(
            text("SELECT id FROM party_donation WHERE id = :id"), {"id": 2}
        )
        return party_donation_id

    # get
    def test_repository_can_retrieve_a_party_donation(self, session):
        party_donation_id = self.insert_party_donation(session)
        factory = SqlAlchemyFactory(session)
        repo = factory.create_party_donation_repository()
        # Act
        retrieved = repo.get("id", party_donation_id)
        expected = models.PartyDonation(
            id=2, amount=1000.0, date=date(2020, 1, 1), party_id=1
        )
        # Assert
        if retrieved is None:
            raise Exception("PartyDonation not found")
        assert retrieved.id == expected.id
        assert retrieved.amount == expected.amount
        assert retrieved.date == expected.date
        # Cleanup
        session.execute(
            text("DELETE FROM party_donation WHERE id = :id"), {"id": party_donation_id}
        )
        session.commit()
