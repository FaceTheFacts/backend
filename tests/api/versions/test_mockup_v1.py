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
import pytest

client = TestClient(app)


@pytest.mark.e2e
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
