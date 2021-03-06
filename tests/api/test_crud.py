import unittest
from unittest.mock import patch

from fastapi import Depends

from src.api.crud import get_politician_by_search
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
