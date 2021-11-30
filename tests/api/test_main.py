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
    assert type(response.json()) is list
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
            "image_url": None
            # TODO add images to S3 bucket and change response to --> "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/108379.jpg",
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
    def whole_values_test():
        response = client.get("/politician/119742/sidejobs?page=1&size=50")
        assert response.status_code == 200
        response_items = [
            {
                "id": 11693,
                "entity_type": "sidejob",
                "label": "Vortrag (Sommergespräch)",
                "income_level": "7.000 € bis 15.000 €",
                "interval": None,
                "data_change_date": "2021-09-10",
                "sidejob_organization": {
                    "id": 2668,
                    "entity_type": "sidejob_organization",
                    "label": "Lupus Alpha Asset Management GmbH",
                },
            },
            {
                "id": 11599,
                "entity_type": "sidejob",
                "label": "Vortrag - Executive Dinner, Donner & Reuschel AG, Hamburg",
                "income_level": "7.000 € bis 15.000 €",
                "interval": None,
                "data_change_date": "2021-08-05",
                "sidejob_organization": {
                    "id": 4086,
                    "entity_type": "sidejob_organization",
                    "label": "Galler & Company",
                },
            },
            {
                "id": 11600,
                "entity_type": "sidejob",
                "label": "Online-Vortrag - Keynote Human-Works-Kongress",
                "income_level": "3.500 € bis 7.000 €",
                "interval": None,
                "data_change_date": "2021-08-05",
                "sidejob_organization": {
                    "id": 4087,
                    "entity_type": "sidejob_organization",
                    "label": "Mercer Deutschland GmbH",
                },
            },
        ]
        for item in response_items:
            assert item in response.json()["items"]

    def selected_values_test():
        response = client.get("/politician/119742/sidejobs?page=1&size=1")
        assert response.status_code == 200
        assert response.json()["items"][0]["sidejob_organization"] == {
            "id": 2668,
            "entity_type": "sidejob_organization",
            "label": "Lupus Alpha Asset Management GmbH",
        }

    def sidejob_not_found_test():
        response = client.get("/politician/28881/sidejobs?page=2&size=1")
        assert response.status_code == 200
        assert response.json() == {"items": [], "total": 0, "page": 2, "size": 1}

    whole_values_test()
    selected_values_test()
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

    label_and_id_test()


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


def test_read_politician_votes():
    def no_filters_random_test():
        response = client.get("/politician/79454/votes")
        test_responses = [
            {
                "Vote": {
                    "id": 410777,
                    "entity_type": "vote",
                    "label": "Dietmar Bartsch - Unternehmerische Sorgfaltspflichten in Lieferketten",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/410777",
                    "mandate_id": 46023,
                    "fraction_id": 41,
                    "poll_id": 4199,
                    "vote": "abstain",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4199,
                    "label": "Unternehmerische Sorgfaltspflichten in Lieferketten",
                    "field_intro": '<p>Der Gesetzentwurf der Bundesregierung soll die Sicherung von Menschenrechten und Umweltstandards für deutsche Unternehmen im internationalen Handel bedeuten. Lieferketten sollen nachweislich fair sein.</p>\r\n\r\n<p>Der Gesetzentwurf wurde mit den Stimmen der Fraktionen CDU/CSU, SPD und B90/DIE GRÜNEN angenommen. Ablehnung erhielt der Entwurf von den Fraktionen AfD und FDP. Entgegen des Fraktionsdrucks stimmten auch 10 Abgeordnete der CDU mit NEIN, darunter <a href="https://www.abgeordnetenwatch.de/profile/axel-eduard-fischer">Axel Eduard Fischer</a>, <a href="https://www.abgeordnetenwatch.de/profile/hans-juergen-irmer">Hans-Jürgen Irmer</a> und <a href="https://www.abgeordnetenwatch.de/profile/andreas-laemmel">Andreas Lämmel</a>. Die Fraktion DIE LINKE enthielt sich, mit Ausnahme von <a href="https://www.abgeordnetenwatch.de/profile/ulla-jelpke">Ulla Jelpke</a>, die mit JA stimmte. Insgesamt stimmten 412 Abgeordnete für den Antrag und 159 Abgeordnete dagegen.</p>\r\n\r\n<p>&nbsp;</p>\r\n',
                    "field_poll_date": "2021-06-11",
                },
            },
        ]

        for item in test_responses:
            assert item in response.json()["items"]

    def response_size_by_filters_test():
        complete_response_total = client.get("/politician/119742/votes").json()["total"]
        single_filter_response_total = client.get(
            "/politician/119742/votes?filters=2"
        ).json()["total"]
        double_filter_response_total = client.get(
            "/politician/119742/votes?filters=2&filters=1"
        ).json()["total"]
        triple_filter_response_total = client.get(
            "/politician/119742/votes?filters=2&filters=1&filters=6"
        ).json()["total"]

        assert complete_response_total >= triple_filter_response_total
        assert triple_filter_response_total >= double_filter_response_total
        assert double_filter_response_total >= single_filter_response_total

    no_filters_random_test()
    response_size_by_filters_test()


def test_read_latest_polls():
    def whole_values_test():
        response = client.get("/bundestag-latest-polls?page=1&size=1")
        assert response.status_code == 200
        response_items = [
            {
                "poll_field_legislature_id": 111,
                "poll_id": 4293,
                "poll_label": "Änderung des Infektionsschutzgesetzes und Grundrechtseinschränkungen",
                "poll_field_poll_date": "2021-09-07",
                "result": {"yes": 344, "no": 280, "abstain": 1, "no_show": 84},
            }
        ]
        for item in response_items:
            assert item in response.json()["items"]

    def selected_values_test():
        response = client.get("/bundestag-latest-polls?page=3&size=1")
        assert response.status_code == 200
        assert response.json()["items"][0]["result"] == {
            "yes": 538,
            "no": 9,
            "abstain": 89,
            "no_show": 73,
        }

    def polls_not_found_test():
        response = client.get("/bundestag-latest-polls?page=100&size=10")
        assert response.status_code == 200
        assert response.json() == {"items": [], "total": 176, "page": 100, "size": 10}

    whole_values_test()
    selected_values_test()
    polls_not_found_test()


def test_read_poll_details():
    def random_test():
        response = client.get("/poll/4217/details")
        assert response.status_code == 200
        response_items = [
            {
                "id": 7585,
                "poll_id": 4217,
                "fraction": {
                    "id": 14,
                    "full_name": "FDP",
                    "short_name": "FDP",
                    "label": "FDP (Bundestag 2017 - 2021)",
                },
                "total_yes": 0,
                "total_no": 71,
                "total_abstain": 0,
                "total_no_show": 9,
            },
            {
                "id": 7590,
                "poll_id": 4217,
                "fraction": {
                    "id": 153,
                    "full_name": "DIE GRÜNEN",
                    "short_name": "DIE GRÜNEN",
                    "label": "DIE GRÜNEN (Bundestag 2017 - 2021)",
                },
                "total_yes": 62,
                "total_no": 0,
                "total_abstain": 0,
                "total_no_show": 5,
            },
        ]
        for item in response_items:
            assert item in response.json()

    def test_unique_fractions_in_response():
        response = client.get("/poll/4174/details")
        fraction_ids = []
        for item in response.json():
            fraction_id = item["fraction"]["id"]
            assert (
                fraction_id not in fraction_ids
            ), f"duplicate fraction of id {fraction_id} in response. All objects must have a unique fraction id"
            fraction_ids.append(fraction_id)

    def test_same_poll_id_in_response():
        poll_id = 713
        response = client.get(f"/poll/{poll_id}/details")

        for item in response.json():
            assert (
                item["poll_id"] == poll_id
            ), f"Item of id {item['id']} is returned with poll_id {item['poll_id']}. Only items with poll_id {poll_id} should be returned"

    random_test()
    test_unique_fractions_in_response()
    test_same_poll_id_in_response()
