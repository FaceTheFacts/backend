import datetime

from src.api.crud import get_all_party_donations


class TestGetAllPartyDonations:
    def test_get_all_party_donations_no_party_ids(self, setup_party_donations):
        session = setup_party_donations
        results = get_all_party_donations(session)
        dates_result = [result.date for result in results]
        # Assert
        assert [
            datetime.date(2023, 1, 1),
            datetime.date(2022, 1, 1),
            datetime.date(2021, 1, 1),
            datetime.date(2020, 1, 1),
        ] == dates_result

    def test_get_all_party_donations_with_party_ids(self, setup_party_donations):
        session = setup_party_donations
        results = get_all_party_donations(session, [1, 2])
        dates_result = [result.date for result in results]
        # Assert
        assert len(results) == 3
        assert [
            datetime.date(2022, 1, 1),
            datetime.date(2021, 1, 1),
            datetime.date(2020, 1, 1),
        ] == dates_result
        assert results[0].party_id == 2

    def test_get_all_party_donations_empty(self, session):
        results = get_all_party_donations(session)
        assert len(results) == 0
