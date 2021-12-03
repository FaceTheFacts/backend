# local
from src.api.main import app
from tests.db.mock_up_database import mockup_session
import src.db.models as models

# default
import unittest
from unittest.mock import patch

# Third-party
from fastapi.testclient import TestClient

client = TestClient(app)


class TestV1Routes(unittest.TestCase):
    # unittest
    @patch(
        "src.api.crud.get_sidejobs_by_politician_id",
        return_value=[
            models.Sidejob(
                id=1,
                entity_type="sidejob",
                label="Member of the County Council",
                income_level="1.000 € bis 3.500 €",
                data_change_date="2021-09-10",
            ),
            models.Sidejob(
                id=2,
                entity_type="sidejob",
                label="Chairman",
                income_level="3.500 € bis 7.000 €",
                data_change_date="2021-09-10",
            ),
        ],
    )
    def test_read_politician_sidejobs(self, crud):
        response = client.get("/v1/politician/1/sidejobs?page=1&size=1")
        assert response.status_code == 200
        expected = [
            {
                "id": 1,
                "entity_type": "sidejob",
                "label": "Member of the County Council",
                "income_level": "1.000 € bis 3.500 €",
                "interval": None,
                "data_change_date": "2021-09-10",
                "sidejob_organization": None,
            }
        ]

        self.assertEqual(response.json()["items"], expected)

    # integration test
    @patch(
        "src.api.versions.v1.Session",
        return_value=mockup_session,
    )
    def test_integration_test_read_politician_sidejobs(self, session):
        response = client.get("/v1/politician/1/sidejobs?page=2&size=1")
        assert response.status_code == 200
        expected = [
            {
                "id": 2,
                "entity_type": "sidejob",
                "label": "Chairman",
                "income_level": "3.500 € bis 7.000 €",
                "interval": None,
                "data_change_date": "2021-09-10",
                "sidejob_organization": None,
            }
        ]
        self.assertEqual(response.json()["items"], expected)


if __name__ == "__main__":
    unittest.main()
