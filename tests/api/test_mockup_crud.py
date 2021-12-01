# default
import unittest

# local
from src.api.crud import get_sidejobs_by_politician_id
from tests.db.mock_up_database import mockup_session
import src.db.models as models


class TestCrudFunctions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCrudFunctions, self).__init__(*args, **kwargs)
        self.session = mockup_session

    def test_get_sidejobs_by_politician_id(self):
        actual = []
        results = get_sidejobs_by_politician_id(self.session, 1)
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


if __name__ == "__main__":
    unittest.main()
