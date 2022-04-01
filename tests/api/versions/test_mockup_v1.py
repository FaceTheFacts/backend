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
                created=1611842082,
            ),
            models.Sidejob(
                id=2,
                entity_type="sidejob",
                label="Chairman",
                income_level="3.500 € bis 7.000 €",
                created=1611842082,
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
                "created": "2021-01-28",
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
                "income_level": None,
                "interval": None,
                "created": "2021-01-28",
                "sidejob_organization": None,
            }
        ]

        print(response.json()["items"][0])

        self.assertEqual(response.json()["items"], expected)
        self.assertEqual(page_not_found_response.json()["detail"], "Sidejobs not found")

    # unittest
    @patch(
        "src.api.crud.get_polls_total",
        return_value=[
            {
                "poll_field_legislature_id": 132,
                "poll_id": 3,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": datetime.datetime(2021, 10, 1),
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
                "politicians": [123456, 135790, 186531, 111111, 153790],
                "last_politician": "Max Mustermann",
            },
            {
                "poll_field_legislature_id": 132,
                "poll_id": 6,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": datetime.datetime(2021, 9, 18),
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
                "politicians": [129456, 135790, 187531, 111311, 153790],
                "last_politician": "Max Mustermann",
            },
        ],
    )
    def test_read_latest_polls(self, crud):
        response = client.get("/v1/bundestag/latest-polls")
        assert response.status_code == 200
        expected = [
            {
                "poll_field_legislature_id": 132,
                "poll_id": 6,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": datetime.datetime(2021, 9, 18),
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
                "politicians": [129456, 135790, 187531, 111311, 153790],
                "last_politician": "Max Mustermann",
            },
        ]
        self.assertEqual(response.json()["items"], expected)

    # integration test
    @patch(
        "src.api.versions.v1.Session",
        return_value=mockup_session,
    )
    def test_integration_test_read_latest_polls(self, session):
        response = client.get("/v1/bundestag/latest-polls")
        assert response.status_code == 200
        expected = [
            {
                "poll_field_legislature_id": 132,
                "poll_id": 3,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": datetime.datetime(2021, 10, 1),
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
                "politicians": [123456, 135790, 186531, 111111, 153790],
                "last_politician": "Max Mustermann",
            },
            {
                "poll_field_legislature_id": 132,
                "poll_id": 6,
                "poll_label": "CDU voting right",
                "poll_field_poll_date": datetime.datetime(2021, 9, 18),
                "result": {"yes": 10, "no": 10, "abstain": 0, "no_show": 2},
                "politicians": [129456, 135790, 187531, 111311, 153790],
                "last_politician": "Max Mustermann",
            },
        ]
        self.assertEqual(response.json()["items"], expected)

    # unittest
    @patch(
        "src.api.crud.get_entity_by_id",
        return_value={
            "id": 119742,
            "positions": [
                {
                    "id": 1281197421,
                    "position": "disagree",
                    "reason": "Ein generelles Tempolimit auf Autobahnen führt weder zu mehr Klimaschutz noch zu mehr Verkehrssicherheit. Anstelle starrer Tempolimits setzen wir auf intelligente Verkehrssysteme. So lässt sich der Verkehr flexibel und digital steuern, um einen nachhaltigeren und sicheren Verkehrsfluss zu erzielen.",
                    "position_statement": {
                        "statement": "Auf den Autobahnen soll ein Tempolimit von 130km/h eingeführt werden."
                    },
                },
                {
                    "id": 1281197422,
                    "position": "disagree",
                    "reason": "Der Schutz der Privatsphäre ist ein Kernanliegen für uns Freie Demokraten. Dennoch brauchen wir einen handlungsfähigen Staat der die Pandemie effektiv und mit modernen, digitalen Mitteln bekämpft. Das ist möglich, ohne unsere hohen Datenschutz-Standards aufzugeben.",
                    "position_statement": {
                        "statement": "Um künftige Pandemien schnell einzudämmen, müssen Einschränkungen beim Datenschutz hingenommen werden."
                    },
                },
            ],
        },
    )
    def test_read_politician_positions(self, positions):
        response = client.get("/v1/politician/119742/positions")
        assert response.status_code == 200
        expected = {
            "id": 119742,
            "positions": [
                {
                    "id": 1281197421,
                    "position": "disagree",
                    "reason": "Ein generelles Tempolimit auf Autobahnen führt weder zu mehr Klimaschutz noch zu mehr Verkehrssicherheit. Anstelle starrer Tempolimits setzen wir auf intelligente Verkehrssysteme. So lässt sich der Verkehr flexibel und digital steuern, um einen nachhaltigeren und sicheren Verkehrsfluss zu erzielen.",
                    "position_statement": {
                        "statement": "Auf den Autobahnen soll ein Tempolimit von 130km/h eingeführt werden."
                    },
                },
                {
                    "id": 1281197422,
                    "position": "disagree",
                    "reason": "Der Schutz der Privatsphäre ist ein Kernanliegen für uns Freie Demokraten. Dennoch brauchen wir einen handlungsfähigen Staat der die Pandemie effektiv und mit modernen, digitalen Mitteln bekämpft. Das ist möglich, ohne unsere hohen Datenschutz-Standards aufzugeben.",
                    "position_statement": {
                        "statement": "Um künftige Pandemien schnell einzudämmen, müssen Einschränkungen beim Datenschutz hingenommen werden."
                    },
                },
            ],
        }
        self.assertEqual(response.json(), expected)


if __name__ == "__main__":
    unittest.main()
