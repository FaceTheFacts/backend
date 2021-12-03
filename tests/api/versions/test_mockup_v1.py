# local
from src.api.main import app
from tests.db.mock_up_database import mockup_session
import src.db.models as models

# default
import unittest
from unittest.mock import patch
import datetime

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
        page_not_found_response = client.get("/v1/politician/0/sidejobs?page=2&size=1")
        assert page_not_found_response.status_code == 404

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
        self.assertEqual(page_not_found_response.json()["detail"], "Sidejobs not found")

    # unittest
    @patch(
        "src.api.crud.get_polls_total",
        return_value=[
            {
                "poll_field_legislature_id": 111,
                "poll_id": 3,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": datetime.datetime(2021, 10, 1),
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
            },
            {
                "poll_field_legislature_id": 132,
                "poll_id": 6,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": datetime.datetime(2021, 9, 18),
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
            },
        ],
    )
    def test_read_latest_polls(self, crud):
        response = client.get("/v1/bundestag-latest-polls?page=1&size=1")
        assert response.status_code == 200
        expected = [
            {
                "poll_field_legislature_id": 111,
                "poll_id": 3,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": "2021-10-01",
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
            },
        ]
        self.assertEqual(response.json()["items"], expected)
    # integration test
    @patch(
        "src.api.versions.v1.Session",
        return_value=mockup_session,
    )
    def test_integration_test_read_latest_polls(self, session):
        response = client.get("/v1/bundestag-latest-polls?page=1&size=2")
        assert response.status_code == 200
        expected = [
            {
                "poll_field_legislature_id": 111,
                "poll_id": 3,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": "2021-10-01",
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
            },
            {
              "poll_field_legislature_id": 111,
              "poll_field_poll_date": "2021-09-27",
              "poll_id": 4,
              "poll_label": "CDU voting right",
              "result": {"abstain": 0, "no": 10, "no_show": 2, "yes": 10},
          }
        ]
        self.assertEqual(response.json()["items"], expected)



if __name__ == "__main__":
    unittest.main()
