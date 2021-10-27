import unittest
from unittest.mock import patch

from fastapi import Depends

from crud import get_politician_by_search
from main import get_db


class TestGetPoliticianBySearch(unittest.TestCase):
    @patch('crud.get_politicians_by_partial_name')
    def test__get_politicians_by_partial_name__is_called(self, mock):
        get_politician_by_search(Depends(get_db), "Marie")
        self.assertTrue(mock.called)

    @patch('crud.get_politicians_by_zipcode')
    def test__get_politicians_by_partial_zipcode__is_called(self, mock):
        get_politician_by_search(Depends(get_db), "54340")
        self.assertTrue(mock.called)
