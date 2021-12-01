import unittest
from unittest import mock
from unittest.mock import patch

from fastapi import Depends

from src.api.crud import get_politician_by_search
from src.api.main import get_db


class TestGetPoliticianBySearch(unittest.TestCase):
    @patch("src.api.crud.get_politicians_by_partial_name")
    def test__get_politicians_by_partial_name__is_called(self, mock):
        get_politician_by_search(Depends(get_db), "Marie")
        self.assertTrue(mock.called)

    @patch("src.api.crud.get_politicians_by_zipcode")
    def test__get_politicians_by_partial_zipcode__is_called(self, mock):
        get_politician_by_search(Depends(get_db), "54340")
        self.assertTrue(mock.called)


from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import src.db.models as models

# session = UnifiedAlchemyMagicMock()
# session.add(models.Politician(id=1, label='bar'))
# session.add(models.Politician(id=2, label='baz'))

# session.add(models.CandidacyMandate(id=1, politician_id=1))
# session.add(models.CandidacyMandate(id=2, politician_id=2))
# session.add(models.SidejobHasMandate(sidejob_id=1, candidacy_mandate_id=1))
# session.add(models.SidejobHasMandate(sidejob_id=2, candidacy_mandate_id=2))
# session.add(models.Sidejob(id=1, label="example1"))
# session.add(models.Sidejob(id=2, label="example2"))


session = UnifiedAlchemyMagicMock(
    data=[
        (
            [
                mock.call.query(models.Politician),
                mock.call.filter(models.Politician.id == 1),
            ],
            [models.Politician(id=1, label="bar")],
        ),
        (
            [
                mock.call.query(models.Politician),
                mock.call.filter(models.Politician.id == 2),
            ],
            [models.Politician(id=2, label="baz")],
        ),
        (
            [
                mock.call.query(models.CandidacyMandate),
                mock.call.filter(
                    models.Politician.id == 1,
                    models.Politician.id == models.CandidacyMandate.politician_id,
                ),
            ],
            [models.CandidacyMandate(id=1, politician_id=1, label="example1")],
        ),
        (
            [
                mock.call.query(models.CandidacyMandate),
                mock.call.filter(
                    models.Politician.id == 2,
                    models.Politician.id == models.CandidacyMandate.politician_id,
                ),
            ],
            [models.CandidacyMandate(id=2, politician_id=2, label="example2")],
        ),
    ]
)


def function1(session, id):

    return (
        session.query(models.CandidacyMandate)
        .filter(models.Politician.id == id)
        .filter(models.Politician.id == models.CandidacyMandate.politician_id)
        .all()
    )


x = function1(session, 2)
print(x[0].label)
