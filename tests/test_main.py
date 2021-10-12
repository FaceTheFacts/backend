from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_poll():
    response = client.get("/poll/1126")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1126,
        "entity_type": "node",
        "label": "Auszahlung von Griechenlandhilfen",
        "api_url": "https://www.abgeordnetenwatch.de/api/v2/polls/1126",
        "committee": {
            "id": 480,
            "entity_type": "node",
            "label": "Ausschuss für Regionale Entwicklung",
            "api_url": "https://www.abgeordnetenwatch.de/api/v2/committees/480",
        },
        "field_intro": '<p>\r\n\tDas Europäische Parlament hat der <a href="http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//NONSGML+TA+P8-TA-2015-0332+0+DOC+PDF+V0//DE">zügigen Umsetzung</a> des Wachstums- und Beschäftigungsplans für Griechenland zugestimmt.\r\n</p>\r\n\r\n<p>\r\n\t<strong>Bitte beachten Sie, dass wir nur das Abstimmungsergebnis für die deutschen EU-Abgeordneten darstellen.</strong>\r\n</p>\r\n',
        "field_poll_date": "2015-10-06",
    }


def test_read_poll_committee_id_null():
    response = client.get("/poll/643")
    assert response.status_code == 200
    assert response.json() == {
        "id": 643,
        "entity_type": "node",
        "label": "Veränderung der Volksgesetzgebung",
        "api_url": "https://www.abgeordnetenwatch.de/api/v2/polls/643",
        "committee": None,
        "field_intro": "Mit 60 zu 56 Stimmen hat die Bürgerschaft eine Veränderung der Volksgesetzgebung beschlossen. Die CDU votierte einstimmig für den Gesetzesentwurf, SPD und GAL dagegen. Der Beschluss sieht u.a. vor, dass das Sammeln von Unterschriften für ein Volksbegehren künftig in Ämtern erfolgen muss und nicht mehr auf der Straße.",
        "field_poll_date": "2005-04-14",
    }


def test_read_poll_not_existing_id():
    response = client.get("/poll/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Poll not found"}
