import unittest
from unittest.mock import patch

from fastapi import Depends

import datetime

from src.api.crud import get_politician_by_search
from src.api.crud import get_party_donations_for_ids_and_time_range
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


class TestGePartyDonationsForIdsAndTimeRange(unittest.TestCase):
    def get_party_donations_for_ids_and_time_range_invalid_time_range(self):
        # query_result = get_party_donations_for_ids_and_time_range(Session, [1], datetime.datetime.now(), datetime.datetime.min)
        self.assertRaises(
            ValueError,
            get_party_donations_for_ids_and_time_range,
            Session,
            [1, 2, 3, 4, 5, 8, 9, 145],
            datetime.datetime.now(),
            datetime.datetime.min,
        )
