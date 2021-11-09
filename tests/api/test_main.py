from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_read_politician():
    def random_test():
        response = client.get("/politician/178104")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.status_code == 200
        assert response.json()["id"] == 178104
        assert response.json()["entity_type"] == "politician"
        assert response.json()["label"] == "Thomas Frost"
        assert response.json()["first_name"] == "Thomas"
        assert response.json()["last_name"] == "Frost"
        assert response.json()["sex"] == "m"
        assert response.json()["year_of_birth"] == "1985"
        assert response.json()["party_past"] is None
        assert response.json()["deceased"] is None
        assert response.json()["deceased_date"] is None
        assert (
            response.json()["education"]
            == "Erzieher/ Kitaleiter, Werkzeugmechaniker, Waffenmechaniker"
        )
        assert response.json()["residence"] == "Mestlin "
        assert response.json()["occupation"] == "Flohmarkt Betreiber "
        assert response.json()["statistic_questions"] is None
        assert response.json()["statistic_questions_answered"] is None
        assert response.json()["qid_wikidata"] is None
        assert response.json()["field_title"] is None

    def specific_elements_test1():
        # Testing past_party, statistic_questions and statistic_questions_answered
        response = client.get("/politician/176101")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["party_past"] == "Vorher Mitglied der Freien Wähler"
        assert response.json()["statistic_questions"] == "10"
        assert response.json()["statistic_questions_answered"] == "9"

    def specific_elements_test_2():
        # Testing deceased, deceased_date and qid_wikidata
        response = client.get("/politician/79107")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["deceased"] is True
        assert response.json()["deceased_date"] == "2020-10-25"
        assert response.json()["qid_wikidata"] == "Q90833"

    def specific_elements_test_3():
        # Testing field_title
        response = client.get("/politician/79109")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["field_title"] == "Dr."

    def votes_and_polls_test():
        response = client.get("/politician/73426?sidejobs_end=0")
        assert response.status_code == 200
        assert type(response.json()) is dict

        votes_and_polls = response.json()["votes_and_polls"]
        assert type(votes_and_polls) is list
        assert len(votes_and_polls) == 5

        for index in range(4):
            assert (
                votes_and_polls[index]["Poll"]["field_poll_date"]
                >= votes_and_polls[index + 1]["Poll"]["field_poll_date"]
            )

    def politician_id_not_found():
        response = client.get("/politician/1")
        assert response.status_code == 404
        assert type(response.json()) is dict
        assert response.json() == {"detail": "Politician not found"}

    random_test()
    specific_elements_test1()
    specific_elements_test_2()
    specific_elements_test_3()
    votes_and_polls_test()
    politician_id_not_found()


def test_read_top_candidates():
    response = client.get("/top-candidates")
    assert response.status_code == 200
    assert type(response.json()) is dict
    assert response.json() == [
        {
            "id": 130072,
            "label": "Armin Laschet",
            "party": {"id": 2, "label": "CDU"},
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/130072.jpg",
        },
        {
            "id": 79475,
            "label": "Annalena Baerbock",
            "party": {"id": 5, "label": "Bündnis 90/Die Grünen"},
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/79475.jpg",
        },
        {
            "id": 66924,
            "label": "Olaf Scholz",
            "party": {"id": 1, "label": "SPD"},
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/66924.jpg",
        },
        {
            "id": 119742,
            "label": "Christian Lindner",
            "party": {"id": 4, "label": "FDP"},
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/119742.jpg",
        },
        {
            "id": 145755,
            "label": "Tino Chrupalla",
            "party": {"id": 9, "label": "AfD"},
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/145755.jpg",
        },
        {
            "id": 108379,
            "label": "Alice Weidel",
            "party": {"id": 9, "label": "AfD"},
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/108379.jpg",
        },
        {
            "id": 135302,
            "label": "Janine Wissler",
            "party": {"id": 8, "label": "DIE LINKE"},
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/135302.jpg",
        },
        {
            "id": 79454,
            "label": "Dietmar Bartsch",
            "party": {"id": 8, "label": "DIE LINKE"},
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/79454.jpg",
        },
    ]


def test_read_politician_constituencies():
    def all_elements_have_values():
        response = client.get("/politician/138540/constituencies")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["candidacy_mandates"].__contains__(
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
        )

    def null_constituencies_exist():
        response = client.get("/politician/138124/constituencies")
        assert response.status_code == 200
        assert type(response.json()) is dict
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


def test_read_politician_positions():
    def selected_values_test():
        response = client.get("/politician/177592/positions")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["positions"].__contains__(
            {
                "id": 1281775921,
                "position": "neutral",
                "reason": "Das hohe Verkehrsaufkommen lässt eine höhere Durchschnittsgeschwindigkeit nach meinem Gefühl nicht zu. das ist rein subjketiv. ",
            }
        )
        assert response.json()["positions"].__contains__(
            {"id": 1281775926, "position": "neutral", "reason": None}
        )

    selected_values_test()


def test_read_politician_sidejobs():
    def selected_values_test():
        response = client.get("/politician/119742/sidejobs?page=1&size=1")
        assert response.status_code == 200
        assert response.json()["items"][0]["sidejob_organization"] == {
            "id": 2668,
            "entity_type": "sidejob_organization",
            "label": "Lupus Alpha Asset Management GmbH",
            "api_url": "https://www.abgeordnetenwatch.de/api/v2/sidejob-organizations/2668",
            "city": {
                "id": 73,
                "entity_type": "taxonomy_term",
                "label": "Frankfurt/Main",
                "api_url": "https://www.abgeordnetenwatch.de/api/v2/cities/73",
            },
            "country": {
                "id": 61,
                "entity_type": "taxonomy_term",
                "label": "Deutschland",
                "api_url": "https://www.abgeordnetenwatch.de/api/v2/countries/61",
            },
            "topics": [
                {
                    "id": 19,
                    "entity_type": "taxonomy_term",
                    "label": "Wirtschaft",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/topics/19",
                    "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/themen-dip21/wirtschaft",
                    "description": None,
                    "parent_id": None,
                },
                {
                    "id": 22,
                    "entity_type": "taxonomy_term",
                    "label": "Öffentliche Finanzen, Steuern und Abgaben",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/topics/22",
                    "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/themen-dip21/oeffentliche-finanzen-steuern-und-abgaben",
                    "description": None,
                    "parent_id": None,
                },
                {
                    "id": 41,
                    "entity_type": "taxonomy_term",
                    "label": "Finanzen",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/topics/41",
                    "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/themen-dip21/finanzen",
                    "description": None,
                    "parent_id": 22,
                },
            ],
        }

    def selected_values_test_2():
        response = client.get("/politician/78808/sidejobs?page=2&size=1")
        assert response.status_code == 200
        assert response.json()["items"][0]["city"] == None
        assert response.json()["items"][0]["country"] == {
            "id": 61,
            "entity_type": "taxonomy_term",
            "label": "Deutschland",
            "api_url": "https://www.abgeordnetenwatch.de/api/v2/countries/61",
        }
        assert response.json()["items"][0]["topics"] == [
            {
                "id": 7,
                "entity_type": "taxonomy_term",
                "label": "Kultur",
                "api_url": "https://www.abgeordnetenwatch.de/api/v2/topics/7",
                "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/themen-dip21/kultur",
                "description": None,
                "parent_id": None,
            }
        ]

    def sidejob_not_found_test():
        response = client.get("/politician/28881/sidejobs?page=2&size=1")
        assert response.status_code == 200
        assert response.json() == {"items": [], "total": 0, "page": 2, "size": 1}

    selected_values_test()
    selected_values_test_2()
    sidejob_not_found_test()


def test_read_politician_image_scanner():
    def label_and_id_test():
        response = client.get("/image-scanner?text=ronald")
        assert response.status_code == 200
        assert type(response.json()) is dict
        test_responses = [
            {"id": 137636, "label": "Ronald Kaufmann"},
            {"id": 124296, "label": "Ronald Maaß"},
            {"id": 124295, "label": "Ronald Doege"},
            {"id": 32270, "label": "Ronald Krügel"},
        ]

        for item in test_responses:
            check_response = False
            for response_item in response.json()["items"]:
                if (
                    item["id"] == response_item["id"]
                    and item["label"] == response_item["label"]
                ):
                    check_response = True
                    break
            assert check_response, "{} item not fount in the response".format(item)

    def pagination_response():
        response = client.get("/image-scanner?text=christian&page=4&size=50")
        assert response.status_code == 200
        assert type(response.json()) is dict

        assert len(response.json()["items"]) == 50
        assert len(response.json()["items"]) == response.json()["size"]

        assert response.json()["page"] == 4

    label_and_id_test()
    pagination_response()


def test_read_politician_search():
    def selected_values_test():
        response = client.get("/search?text=55278")
        assert response.status_code == 200
        assert type(response.json()) is dict
        test_responses = [
            {"id": 177457, "label": "Chiara Pohl"},
            {"id": 175546, "label": "Christian Engelke"},
            {"id": 176888, "label": "David Hess"},
        ]

        for item in test_responses:
            check_response = False
            for response_item in response.json()["items"]:
                if (
                        item["id"] == response_item["id"]
                        and item["label"] == response_item["label"]
                ):
                    check_response = True
                    break
            assert check_response, "{} item not fount in the response".format(item)

    selected_values_test()


# combined test for read_politician_search and read_politicians_image_scanner
def test_search_and_image_scanner():
    search_response = client.get("/search?text=Philipp")
    image_scanner_response = client.get("image-scanner?text=Philipp")

    assert search_response.json() == image_scanner_response.json()
