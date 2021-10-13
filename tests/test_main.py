from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_poll():
    def all_elements_have_values():
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

    def committee_id_null():
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

    def poll_id_not_found():
        response = client.get("/poll/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Poll not found"}

    all_elements_have_values()
    committee_id_null()
    poll_id_not_found()


def test_read_politician():
    def random_test():
        response = client.get("/politician/178104")
        assert response.status_code == 200
        assert response.json() == {
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

    def specific_elements_test1():
        # Testing past_party, statistic_questions and statistic_questions_answered
        response = client.get("/politician/176101")
        assert response.status_code == 200
        assert response.json() == {
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

    def specific_elements_test_2():
        # Testing deceased, deceased_date and qid_wikidata
        response = client.get("/politician/79107")
        assert response.status_code == 200
        assert response.json() == {
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

    def specific_elements_test_3():
        # Testing field_title
        response = client.get("/politician/79109")
        assert response.status_code == 200
        assert response.json() == {
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

    def politician_id_not_found():
        response = client.get("/politician/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Politician not found"}

    random_test()
    specific_elements_test1()
    specific_elements_test_2()
    specific_elements_test_3()
    politician_id_not_found()


def test_read_politician_constituencies():
    def all_elements_have_values():
        response = client.get("/politician/138540/constituencies")
        assert response.status_code == 200
        assert response.json() == {
            "id": 138540,
            "candidacy_mandates": [
                {
                    "id": 54370,
                    "electoral_data": {
                        "id": 55294,
                        "constituency": {
                            "id": 11039,
                            "entity_type": "constituency",
                            "label": "299 - Homburg (Bundestag 2021 - 2025)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/11039",
                            "name": "Homburg",
                            "number": 299,
                        },
                    },
                },
                {
                    "id": 49967,
                    "electoral_data": {
                        "id": 50889,
                        "constituency": {
                            "id": 10356,
                            "entity_type": "constituency",
                            "label": "299 - Homburg (Bundestag Wahl 2021)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/10356",
                            "name": "Homburg",
                            "number": 299,
                        },
                    },
                },
                {
                    "id": 43643,
                    "electoral_data": {
                        "id": 43643,
                        "constituency": {
                            "id": 4423,
                            "entity_type": "constituency",
                            "label": "299 - Homburg (Bundestag 2017 - 2021)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/4423",
                            "name": "Homburg",
                            "number": 299,
                        },
                    },
                },
                {
                    "id": 43642,
                    "electoral_data": {
                        "id": 43642,
                        "constituency": {
                            "id": 1171,
                            "entity_type": "constituency",
                            "label": "299 - Homburg (Bundestag 2013-2017)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/1171",
                            "name": "Homburg",
                            "number": 299,
                        },
                    },
                },
                {
                    "id": 28413,
                    "electoral_data": {
                        "id": 28413,
                        "constituency": {
                            "id": 9309,
                            "entity_type": "constituency",
                            "label": "299 - Homburg (Bundestag Wahl 2017)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/9309",
                            "name": "Homburg",
                            "number": 299,
                        },
                    },
                },
                {
                    "id": 28412,
                    "electoral_data": {
                        "id": 28412,
                        "constituency": {
                            "id": 9309,
                            "entity_type": "constituency",
                            "label": "299 - Homburg (Bundestag Wahl 2017)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/9309",
                            "name": "Homburg",
                            "number": 299,
                        },
                    },
                },
                {
                    "id": 28411,
                    "electoral_data": {
                        "id": 28411,
                        "constituency": {
                            "id": 9309,
                            "entity_type": "constituency",
                            "label": "299 - Homburg (Bundestag Wahl 2017)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/9309",
                            "name": "Homburg",
                            "number": 299,
                        },
                    },
                },
                {
                    "id": 28410,
                    "electoral_data": {
                        "id": 28410,
                        "constituency": {
                            "id": 5297,
                            "entity_type": "constituency",
                            "label": "2 - Neunkirchen (Saarland Wahl 2009)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/5297",
                            "name": "Neunkirchen",
                            "number": 2,
                        },
                    },
                },
            ],
        }

    def null_constituencies_exist():
        response = client.get("/politician/138124/constituencies")
        assert response.status_code == 200
        assert response.json() == {
            "id": 138124,
            "candidacy_mandates": [
                {"id": 54372, "electoral_data": {"id": 55296, "constituency": None}},
                {
                    "id": 49849,
                    "electoral_data": {
                        "id": 50771,
                        "constituency": {
                            "id": 10353,
                            "entity_type": "constituency",
                            "label": "296 - Saarbrücken (Bundestag Wahl 2021)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/constituencies/10353",
                            "name": "Saarbrücken",
                            "number": 296,
                        },
                    },
                },
                {"id": 43613, "electoral_data": {"id": 43613, "constituency": None}},
                {"id": 27911, "electoral_data": {"id": 27911, "constituency": None}},
                {"id": 27910, "electoral_data": {"id": 27910, "constituency": None}},
            ],
        }

    all_elements_have_values()
    null_constituencies_exist()
