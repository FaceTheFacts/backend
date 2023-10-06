import unittest
from unittest.mock import patch
import datetime

from fastapi import Depends


from src.api.crud import (
    get_politician_by_search,
    get_party_donations_for_ids_and_time_range,
    build_donation_data_response_object,
    build_donations_over_time_container,
    get_all_party_donations,
)
from src.db.connection import Session

session = Session()


class TestGetPoliticianBySearch(unittest.TestCase):
    @patch("src.api.crud.get_politicians_by_partial_name")
    def test__get_politicians_by_partial_name__is_called(self, mock):
        get_politician_by_search(Depends(session), "Marie")
        self.assertTrue(mock.called)

    @patch("src.api.crud.get_politicians_by_zipcode")
    def test__get_politicians_by_partial_zipcode__is_called(self, mock):
        get_politician_by_search(Depends(session), "54340")
        self.assertTrue(mock.called)


class TestGetPartyDonationsForIdsAndTimeRange(unittest.TestCase):
    # def test_get_party_donations_for_ids_and_time_range_single_party(self):
    #     donations = get_party_donations_for_ids_and_time_range(
    #         session,
    #         [4],
    #         datetime.datetime(2021, 4, 24),
    #         datetime.datetime(2021, 5, 24),
    #     )
    #     assert len(donations) == 2

    # def test_get_party_donations_for_ids_and_time_range_multiple_parties(self):
    #     donations = get_party_donations_for_ids_and_time_range(
    #         session,
    #         [4, 2],
    #         datetime.datetime(2021, 4, 24),
    #         datetime.datetime(2021, 5, 24),
    #     )
    #     assert len(donations) == 4

    def test_get_party_donations_for_ids_and_time_range_invalid_time_range(self):
        self.assertRaises(
            ValueError,
            get_party_donations_for_ids_and_time_range,
            session,
            [1, 2, 3, 4, 5, 8, 9, 145],
            datetime.datetime(2022, 5, 25),
            datetime.datetime(2022, 5, 24),
        )

    def test_build_donation_data_response_object(self):
        response_object = build_donation_data_response_object([4, 33])

        assert response_object == [
            {
                "id": 4,
                "party": None,
                "donations_over_32_quarters": [],
                "donations_total": 0,
                "largest_quarter": None,
            },
            {
                "id": 33,
                "party": None,
                "donations_over_32_quarters": [],
                "donations_total": 0,
                "largest_quarter": None,
            },
        ]

    def test_build_donations_over_time_container_length(self):
        donation_over_quarters = build_donations_over_time_container([3, 5], 32)

        assert (
            len(donation_over_quarters[3]) == 32
            and len(donation_over_quarters[5]) == 32
        )

    def test_build_donations_over_time_container_values(self):
        donation_over_quarters = build_donations_over_time_container([2, 4], 20)

        assert (
            sum(donation_over_quarters[2]) == 0 and sum(donation_over_quarters[4]) == 0
        )


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
