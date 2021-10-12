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
        "committee": {
            "id": 480,
            "entity_type": "node",
            "label": "Ausschuss für Regionale Entwicklung",
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
        "committee": None,
        "field_intro": "Mit 60 zu 56 Stimmen hat die Bürgerschaft eine Veränderung der Volksgesetzgebung beschlossen. Die CDU votierte einstimmig für den Gesetzesentwurf, SPD und GAL dagegen. Der Beschluss sieht u.a. vor, dass das Sammeln von Unterschriften für ein Volksbegehren künftig in Ämtern erfolgen muss und nicht mehr auf der Straße.",
        "field_poll_date": "2005-04-14",
    }


def test_read_poll_not_existing_id():
    response = client.get("/poll/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Poll not found"}


def test_read_politician():
    # Random Test
    response1 = client.get("/politician/178104")
    assert response1.status_code == 200
    assert response1.json() == {
        "id": 178104,
        "entity_type": "politician",
        "label": "Thomas Frost",
        "first_name": "Thomas",
        "last_name": "Frost",
        "sex": "m",
        "year_of_birth": "1985",
        "party_past": None,
        "deceased": None,
        "deceased_date": None,
        "education": "Erzieher/ Kitaleiter, Werkzeugmechaniker, Waffenmechaniker",
        "residence": "Mestlin ",
        "occupation": "Flohmarkt Betreiber ",
        "statistic_questions": None,
        "statistic_questions_answered": None,
        "qid_wikidata": None,
        "field_title": None,
    }

    # Testing past_party, statistic_questions and statistic_questions_answered
    response2 = client.get("/politician/176101")
    assert response1.status_code == 200
    assert response2.json() == {
        "id": 176101,
        "entity_type": "politician",
        "label": "Felix Locke",
        "first_name": "Felix",
        "last_name": "Locke",
        "sex": "m",
        "year_of_birth": "1988",
        "party_past": "Vorher Mitglied der Freien Wähler",
        "deceased": None,
        "deceased_date": None,
        "education": "B.A.",
        "residence": "Lauf an der Pegnitz",
        "occupation": "Konzernprojektleiter",
        "statistic_questions": "10",
        "statistic_questions_answered": "9",
        "qid_wikidata": None,
        "field_title": None,
    }

    # Testing deceased, deceased_date and qid_wikidata
    response2 = client.get("/politician/79107")
    assert response1.status_code == 200
    assert response2.json() == {
        "id": 79107,
        "entity_type": "politician",
        "label": "Thomas Oppermann",
        "first_name": "Thomas",
        "last_name": "Oppermann",
        "sex": "m",
        "year_of_birth": "1954",
        "party_past": None,
        "deceased": True,
        "deceased_date": "2020-10-25",
        "education": "Jurist",
        "residence": None,
        "occupation": "MdB",
        "statistic_questions": "266",
        "statistic_questions_answered": "260",
        "qid_wikidata": "Q90833",
        "field_title": None,
    }

    # Testing field_title
    response2 = client.get("/politician/79109")
    assert response1.status_code == 200
    assert response2.json() == {
        "id": 79109,
        "entity_type": "politician",
        "label": "Alexander S. Neu",
        "first_name": "Alexander S.",
        "last_name": "Neu",
        "sex": "m",
        "year_of_birth": "1969",
        "party_past": None,
        "deceased": None,
        "deceased_date": None,
        "education": "Politikwissenschaftler",
        "residence": None,
        "occupation": "MdB",
        "statistic_questions": "32",
        "statistic_questions_answered": "29",
        "qid_wikidata": "Q15434455",
        "field_title": "Dr.",
    }


def test_read_politician_not_existing_id():
    response = client.get("/politician/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politician not found"}
