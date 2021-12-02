# default
import unittest
from unittest.mock import patch
import datetime

# local
import src.api.crud as crud
from tests.db.mock_up_database import mockup_session


class TestCrudFunctions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCrudFunctions, self).__init__(*args, **kwargs)
        self.session = mockup_session

    def test_get_sidejobs_by_politician_id(self):
        actual = []
        results = crud.get_sidejobs_by_politician_id(self.session, 1)
        for result in results:
            item = {
                "id": result.id,
                "label": result.label,
                "income_level": result.income_level,
            }
            actual.append(item)
        expected = [
            {
                "id": 1,
                "label": "Member of the County Council",
                "income_level": "1.000 € bis 3.500 €",
            },
            {
                "id": 2,
                "label": "Chairman",
                "income_level": "3.500 € bis 7.000 €",
            },
        ]

        self.assertListEqual(actual, expected)

    def test_get_latest_bundestag_polls(self):
        actual = []
        results = crud.get_latest_bundestag_polls(self.session)
        for result in results:
            item = {
                "id": result.id,
                "field_legislature_id": result.field_legislature_id,
                "field_poll_date": result.field_poll_date,
            }
            actual.append(item)
        expected = [
            {
                "id": 3,
                "field_legislature_id": 111,
                "field_poll_date": datetime.datetime(2021, 10, 1),
            },
            {
                "id": 4,
                "field_legislature_id": 111,
                "field_poll_date": datetime.datetime(2021, 9, 27),
            },
            {
                "id": 5,
                "field_legislature_id": 132,
                "field_poll_date": datetime.datetime(2021, 9, 20),
            },
            {
                "id": 6,
                "field_legislature_id": 132,
                "field_poll_date": datetime.datetime(2021, 9, 18),
            },
        ]
        self.assertEqual(actual, expected)

    def test_get_vote_result_by_poll_id(self):
        result = crud.get_vote_result_by_poll_id(self.session, 3)
        actual = {
            "id": result.id,
            "yes": result.yes,
            "no": result.no,
            "abstain": result.abstain,
            "no_show": result.no_show,
            "poll_id": result.poll_id,
        }
        expected = {
            "id": 1,
            "yes": 10,
            "no": 10,
            "abstain": 0,
            "no_show": 2,
            "poll_id": 3,
        }
        not_expected = {
            "id": 3,
            "yes": 10,
            "no": 10,
            "abstain": 0,
            "no_show": 2,
            "poll_id": 10,
        }
        self.assertEqual(actual, expected)
        self.assertNotEqual(actual, not_expected)

    # @patch(
    #     "src.api.crud.get_latest_bundestag_polls",
    #     return_value=[
    #         {
    #             "id": 3,
    #             "poll_id": 100,
    #             "label": "CDU voting right",
    #             "field_legislature_id": 111,
    #             "field_poll_date": datetime.datetime(2021, 10, 1),
    #         }
    #     ],
    # )
    # @patch(
    #     "src.api.crud.get_vote_result_by_poll_id",
    #     return_value=[{"yes": 10, "no": 10, "abstain": 0, "no_show": 2}],
    # )
    # def test_get_polls_total(self, mock_get_latest_bundestag_polls, mock_get_vote_result_by_poll_id):
    #     actual = crud.get_polls_total(self.session)
    #     expected = [
    #         {
    #             "poll_field_legislature_id": 111,
    #             "poll_id": 100,
    #             "poll_label": "CDU voting right",
    #             "poll_field_poll_date": datetime.datetime(2021, 10, 1),
    #             "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
    #         }
    #     ]
    #     self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
