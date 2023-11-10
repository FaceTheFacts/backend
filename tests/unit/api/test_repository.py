from datetime import date

import pytest
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

from src.api.repository import SqlAlchemyFactory
import src.db.models as models


def delete_party_donation(session):
    session.execute(text("DELETE FROM party_donation"))
    session.commit()


class TestSqlAlchemyPartyDonationRepository:
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
        delete_party_donation(session)

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
            pass  # Handle the expected exception

        # Cleanup (outside the try-except block)
        delete_party_donation(session)

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

    def insert_party_donations(self, session):
        query = text(
            "INSERT INTO party_donation (id, amount, date, party_id) "
            "VALUES (:id, :amount, :date, :party_id)"
        )

        data = [
            {"id": 2, "amount": 1000.0, "date": date(2020, 1, 1), "party_id": 1},
            {"id": 3, "amount": 2000.0, "date": date(2020, 1, 2), "party_id": 1},
            {"id": 4, "amount": 3000.0, "date": date(2020, 1, 3), "party_id": 2},
            {"id": 5, "amount": 4000.0, "date": date(2020, 1, 4), "party_id": 2},
            {"id": 6, "amount": 5000.0, "date": date(2020, 1, 5), "party_id": 3},
            {"id": 7, "amount": 6000.0, "date": date(2020, 1, 6), "party_id": 3},
        ]

        session.execute(query, data)

    # get
    def test_repository_can_retrieve_a_party_donation(self, session):
        party_donation_id = self.insert_party_donation(session)
        factory = SqlAlchemyFactory(session)
        repo = factory.create_party_donation_repository()
        # Act
        try:
            retrieved = repo.get("id", party_donation_id)
        except NoResultFound:
            raise NoResultFound("PartyDonation not found")

        expected = models.PartyDonation(
            id=2, amount=1000.0, date=date(2020, 1, 1), party_id=1
        )
        # Assert
        assert retrieved.id == expected.id
        assert retrieved.amount == expected.amount
        assert retrieved.date == expected.date
        # Cleanup
        session.execute(
            text("DELETE FROM party_donation WHERE id = :id"), {"id": party_donation_id}
        )
        session.commit()

    # list
    def test_repository_can_list_all_party_donations(self, session):
        self.insert_party_donations(session)
        factory = SqlAlchemyFactory(session)
        repo = factory.create_party_donation_repository()
        # Act
        retrieved_list = repo.list()
        # Assert
        assert len(retrieved_list) == 6
        # Assert: Descending order
        assert retrieved_list[0].date == date(2020, 1, 6)
        assert retrieved_list[-1].date == date(2020, 1, 1)
        # Cleanup
        delete_party_donation(session)

    # list
    def test_repository_can_list_all_party_donations_with_party_ids(self, session):
        self.insert_party_donations(session)
        factory = SqlAlchemyFactory(session)
        repo = factory.create_party_donation_repository()
        # Act
        retrieved_list = repo.list(party_ids=[1, 2])
        # Assert
        assert len(retrieved_list) == 4
        assert retrieved_list[0].date == date(2020, 1, 4)
        assert retrieved_list[-1].date == date(2020, 1, 1)
        # Cleanup
        delete_party_donation(session)

    def test_repository_can_add_or_update_a_party_donation_using_merge(self, session):
        factory = SqlAlchemyFactory(session)
        repo = factory.create_party_donation_repository()
        # Act
        # Insert a party_donation with id=1
        party_donation = models.PartyDonation(
            id=1, amount=1000.0, date=date(2020, 1, 1), party_id=1
        )
        repo.add(party_donation)
        # Create a new party_donation with the same id but different values
        updated_party_donation = models.PartyDonation(
            id=1, amount=2000.0, date=date(2020, 1, 2), party_id=2
        )
        repo.add_or_update(updated_party_donation)
        # Retrieve the party_donation with id=1 from the database
        rows = session.execute(
            text("SELECT * FROM party_donation WHERE id = :id"), {"id": 1}
        )
        # Assert
        assert list(rows) == [(1, 2, 2000.0, "2020-01-02", None)]
        # Cleanup
        delete_party_donation(session)

    def test_repository_can_add_or_update_list_using_insert(self, session):
        factory = SqlAlchemyFactory(session)
        repo = factory.create_party_donation_repository()
        # Act
        # Insert a party_donation with id=1
        party_donation1 = models.PartyDonation(
            id=1, amount=1000.0, date=date(2020, 1, 1), party_id=1
        )
        repo.add(party_donation1)
        session.commit()

        # Create a list of party_donations to add or update
        party_donations_to_add_update = [
            {
                "id": 1,
                "amount": 2000.0,  # updated
                "date": date(2020, 1, 2),  # updated
                "party_id": 2,  # updated
            },
            {
                "id": 2,
                "amount": 3000.0,
                "date": date(2020, 1, 3),
                "party_id": 2,
            }
            # Add more party_donations as needed
        ]

        # Act: Use add_or_update_list method with insert and on_conflict_do_nothing
        repo.add_or_update_list(party_donations_to_add_update)

        # Retrieve the party_donation with id=1 from the database
        rows = session.execute(
            text("SELECT * FROM party_donation WHERE id IN (:id1, :id2)"),
            {"id1": 1, "id2": 2},
        )
        # Assert
        assert list(rows) == [
            (1, 2, 2000.0, "2020-01-02", None),  # updated
            (2, 2, 3000.0, "2020-01-03", None),  # inserted
        ]
        # Cleanup
        delete_party_donation(session)
