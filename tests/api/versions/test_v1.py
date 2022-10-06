from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)
#### GENERAL NOTES ####

# Potential things to consider:
# status of entity (retired/active, will fields change?)
# size of lists/dicts (what are the default boundaries? 0-what?)
# testing variations of the parameters (e.g. for start/end size or paginations)
# testing negatives (missing resource)
# testing missing routes: politicianshistory, poll/id/votes, bundestag/speeches, bundestag/polls, bundestag/allpolls, partydonations


def test_read_politician():
    # update method name
    def random_test():
        # replace with politician ID of someone retired and with all fields filled out if possible
        response = client.get("/v1/politician/178104")
        assert response.status_code == 200
        assert type(response.json()) is dict  # unecessary, .json() only returns dicts?
        assert response.status_code == 200
        # serialize response once and use that to check for values instead of repeating the same code
        assert response.json()["id"] == 178104
        assert response.json()["label"] == "Thomas Frost"
        assert response.json()["occupations"] == ["Flohmarkt Betreiber"]
        assert response.json()["sidejobs"] == []
        assert response.json()["cvs"] == []
        assert (
            response.json()["abgeordnetenwatch_url"]
            == "https://www.abgeordnetenwatch.de/profile/thomas-frost"
        )
        assert response.json()["weblinks"] == [
            {
                "id": 31117,
                "link": "https://www.thomasfrost.de/",
                "politician_id": 178104,
            },
            {
                "id": 31118,
                "link": "https://www.facebook.com/familieumweltartenschutz/",
                "politician_id": 178104,
            },
        ]
        assert response.json()["votes_and_polls"] == []
        assert response.json()["topic_ids_of_latest_committee"] == []

    # redundant
    def weblinks_test():
        response = client.get("/v1/politician/176101")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["weblinks"] == [
            {
                "id": 32294,
                "link": "https://www.felix-locke.de",
                "politician_id": 176101,
            },
            {
                "id": 32295,
                "link": "https://de.wikipedia.org/wiki/Felix_Locke",
                "politician_id": 176101,
            },
            {
                "id": 32296,
                "link": "https://www.instagram.com/felix_locke_fw/",
                "politician_id": 176101,
            },
            {
                "id": 32297,
                "link": "https://www.facebook.com/LockeFW",
                "politician_id": 176101,
            },
            {
                "id": 32298,
                "link": "https://twitter.com/felix_locke_fw",
                "politician_id": 176101,
            },
        ]

    # redundant
    def cv_test():
        response = client.get("/v1/politician/79109")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["cvs"] == [
            {
                "id": 560,
                "short_description": "Geboren am 19. März 1969; verheiratet; zwei Kinder.",
                "raw_text": "Abitur in Siegburg; Studium der politischen Wissenschaft an der Friedrich-Wilhems-Universität in Bonn; Promotion 2004; 2000 bis 2002 und 2004 Auslandstätigkeit in der Organisation für Sicherheit und Zusammenarbeit in Europa (OSZE) im ehemaligen Jugoslawien; 2006 bis 2013 Referent für Sicherheitspolitik bei der Fraktion DIE LINKE.\xa0 ",
                "politician_id": 79109,
            }
        ]

    # redundant
    def abgeordnetenwatch_url_test():
        response = client.get("/v1/politician/79107")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert (
            response.json()["abgeordnetenwatch_url"]
            == "https://www.abgeordnetenwatch.de/profile/thomas-oppermann"
        )

    def votes_and_polls_test():
        response = client.get(
            "/v1/politician/73426?sidejobs_end=0"
        )  # What is this parameter for sidejobs_end?

        assert response.status_code == 200
        assert type(response.json()) is dict

        votes_and_polls = response.json()["votes_and_polls"]
        assert type(votes_and_polls) is list  # constrained by Schema?
        assert (
            len(votes_and_polls) == 6
        )  # default value, should test the boundaries too

        # testing order of results (might be useful elsewhere too)
        for index in range(4):
            assert (
                votes_and_polls[index]["Poll"]["field_poll_date"]
                >= votes_and_polls[index + 1]["Poll"]["field_poll_date"]
            )

    def politician_id_not_found():
        response = client.get("/v1/politician/1")
        assert response.status_code == 404
        assert type(response.json()) is dict  # unecessary
        assert response.json() == {"detail": "Politician not found"}

    def occupations_test():
        response = client.get("/v1/politician/130072")
        response_items = ["MdB"]

        for item in response_items:
            assert item in response.json()["occupations"]

    def test_topic_ids_of_latest_committee():
        response = client.get("/v1/politician/131019")
        expected_ids = [11, 19]
        assert expected_ids == response.json()["topic_ids_of_latest_committee"]

        response = client.get("/v1/politician/139064")
        expected_ids = [9, 11, 19, 20]
        assert expected_ids == response.json()["topic_ids_of_latest_committee"]

    random_test()
    weblinks_test()
    cv_test()
    abgeordnetenwatch_url_test()
    votes_and_polls_test()
    politician_id_not_found()
    occupations_test()
    test_topic_ids_of_latest_committee()


def test_read_politician_constituencies():
    def all_elements_have_values():
        response = client.get("/v1/politician/138540/constituencies")
        assert response.status_code == 200
        assert type(response.json()) is dict  # unecessary
        # maybe shift out into another file
        assert response.json() == {
            "constituency_number": 299,
            "constituency_name": "Homburg",
            "politicians": [
                {
                    "id": 138540,
                    "label": "Markus Uhl",
                    "party": {
                        "id": 2,
                        "label": "CDU",
                        "party_style": {
                            "id": 2,
                            "display_name": "CDU",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#636363",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 138463,
                    "label": "Esra Limbacher",
                    "party": {
                        "id": 1,
                        "label": "SPD",
                        "party_style": {
                            "id": 1,
                            "display_name": "SPD",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#E95050",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 138292,
                    "label": "Maria Luise Herber",
                    "party": {
                        "id": 5,
                        "label": "Bündnis 90/Die Grünen",
                        "party_style": {
                            "id": 5,
                            "display_name": "Grüne",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#61A056",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 175796,
                    "label": "Ralf Armbrüster",
                    "party": {
                        "id": 4,
                        "label": "FDP",
                        "party_style": {
                            "id": 4,
                            "display_name": "FDP",
                            "foreground_color": "#333333",
                            "background_color": "#FAED0B",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 177232,
                    "label": "Florian Spaniol",
                    "party": {
                        "id": 8,
                        "label": "DIE LINKE",
                        "party_style": {
                            "id": 8,
                            "display_name": "Linke",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#CD3E72",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 150296,
                    "label": "Christian-Friedrich Wirth",
                    "party": {
                        "id": 9,
                        "label": "AfD",
                        "party_style": {
                            "id": 9,
                            "display_name": "AfD",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#3AA6F4",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 177853,
                    "label": "Ute Elisabeth Weisang",
                    "party": {
                        "id": 201,
                        "label": "dieBasis",
                        "party_style": {
                            "id": 201,
                            "display_name": "dieBasis",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#333333",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 176099,
                    "label": "Evelyne Görlinger",
                    "party": {
                        "id": 16,
                        "label": "Die PARTEI",
                        "party_style": {
                            "id": 16,
                            "display_name": "Die PARTEI",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#722B2B",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 176057,
                    "label": "Claus Jacob",
                    "party": {
                        "id": 12,
                        "label": "ÖDP",
                        "party_style": {
                            "id": 12,
                            "display_name": "ÖDP",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#FD820B",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 147500,
                    "label": "Axel Kammerer",
                    "party": {
                        "id": 7,
                        "label": "FREIE WÄHLER",
                        "party_style": {
                            "id": 7,
                            "display_name": "FREIE WÄHLER",
                            "foreground_color": "#2F5997",
                            "background_color": "#F8F8F8",
                            "border_color": "#FD820B",
                        },
                    },
                },
            ],
        }

    def null_constituencies_exist():
        response = client.get("/v1/politician/138124/constituencies")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json() == {
            "constituency_number": 296,
            "constituency_name": "Saarbrücken",
            "politicians": [
                {
                    "id": 138124,
                    "label": "Annegret Kramp-Karrenbauer",
                    "party": {
                        "id": 2,
                        "label": "CDU",
                        "party_style": {
                            "id": 2,
                            "display_name": "CDU",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#636363",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 146867,
                    "label": "Josephine Ortleb",
                    "party": {
                        "id": 1,
                        "label": "SPD",
                        "party_style": {
                            "id": 1,
                            "display_name": "SPD",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#E95050",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 164999,
                    "label": "Gerhard Wenz",
                    "party": {
                        "id": 5,
                        "label": "Bündnis 90/Die Grünen",
                        "party_style": {
                            "id": 5,
                            "display_name": "Grüne",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#61A056",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 175734,
                    "label": "Helmut Isringhaus",
                    "party": {
                        "id": 4,
                        "label": "FDP",
                        "party_style": {
                            "id": 4,
                            "display_name": "FDP",
                            "foreground_color": "#333333",
                            "background_color": "#FAED0B",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 177566,
                    "label": "Boris Huebner",
                    "party": {
                        "id": 9,
                        "label": "AfD",
                        "party_style": {
                            "id": 9,
                            "display_name": "AfD",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#3AA6F4",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 177230,
                    "label": "Mark Baumeister",
                    "party": {
                        "id": 8,
                        "label": "DIE LINKE",
                        "party_style": {
                            "id": 8,
                            "display_name": "Linke",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#CD3E72",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 177845,
                    "label": "Steffi Richter",
                    "party": {
                        "id": 201,
                        "label": "dieBasis",
                        "party_style": {
                            "id": 201,
                            "display_name": "dieBasis",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#333333",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 148443,
                    "label": "Rolf Tickert",
                    "party": {
                        "id": 15,
                        "label": "MLPD",
                        "party_style": {
                            "id": 15,
                            "display_name": "MLPD",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#333333",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 177290,
                    "label": "Stephan Poss",
                    "party": {
                        "id": 185,
                        "label": "parteilos",
                        "party_style": {
                            "id": 185,
                            "display_name": "parteilos",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#333333",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 176255,
                    "label": "Nico Herrmann",
                    "party": {
                        "id": 12,
                        "label": "ÖDP",
                        "party_style": {
                            "id": 12,
                            "display_name": "ÖDP",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#FD820B",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 176204,
                    "label": "Luman Matheis Lukas",
                    "party": {
                        "id": 16,
                        "label": "Die PARTEI",
                        "party_style": {
                            "id": 16,
                            "display_name": "Die PARTEI",
                            "foreground_color": "#FFFFFF",
                            "background_color": "#722B2B",
                            "border_color": None,
                        },
                    },
                },
                {
                    "id": 176123,
                    "label": "Hans-Peter Pflug",
                    "party": {
                        "id": 7,
                        "label": "FREIE WÄHLER",
                        "party_style": {
                            "id": 7,
                            "display_name": "FREIE WÄHLER",
                            "foreground_color": "#2F5997",
                            "background_color": "#F8F8F8",
                            "border_color": "#FD820B",
                        },
                    },
                },
            ],
        }

    all_elements_have_values()
    null_constituencies_exist()


def test_read_politician_positions():
    def selected_values_test():
        response = client.get("/v1/politician/177592/positions")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["positions"].__contains__(
            {
                "id": 1281775921,
                "position": "neutral",
                "reason": "Das hohe Verkehrsaufkommen lässt eine höhere Durchschnittsgeschwindigkeit nach meinem Gefühl nicht zu. das ist rein subjketiv. ",
                "position_statement": {
                    "statement": "Auf den Autobahnen soll ein Tempolimit von 130km/h eingeführt werden."
                },
            }
        )
        assert response.json()["positions"].__contains__(
            {
                "id": 1281775926,
                "position": "neutral",
                "reason": None,
                "position_statement": {
                    "statement": "Der öffentlich-rechtliche Rundfunk soll sich auf Information und regionale Berichterstattung konzentrieren."
                },
            }
        )

    selected_values_test()


def test_read_politician_sidejobs():
    def whole_values_test():
        response = client.get("/v1/politician/119742/sidejobs?page=1&size=50")
        assert response.status_code == 200
        response_items = [
            {
                "id": 11693,
                "entity_type": "sidejob",
                "label": "Vortrag (Sommergespräch)",
                "income_level": "7.000 € bis 15.000 €",
                "interval": None,
                "created": "2021-09-10",
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
                "created": "2021-08-05",
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
                "created": "2021-08-05",
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
        response = client.get("/v1/politician/119742/sidejobs?page=1&size=1")
        assert response.status_code == 200
        assert response.json()["items"][0]["sidejob_organization"] == {
            "id": 2668,
            "entity_type": "sidejob_organization",
            "label": "Lupus Alpha Asset Management GmbH",
        }

    def sidejob_not_found_test():
        response = client.get("/v1/politician/28881/sidejobs?page=2&size=1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Sidejobs not found"}

    whole_values_test()
    selected_values_test()
    sidejob_not_found_test()


def test_read_politician_image_scanner():
    def label_and_id_test():
        response = client.get("/v1/image-scanner?id=79334")
        assert response.status_code == 200
        assert type(response.json()) is list
        test_responses = [
            {
                "id": 79334,
                "label": "Gregor Gysi",
                "party": {
                    "id": 8,
                    "label": "DIE LINKE",
                    "party_style": {
                        "id": 8,
                        "display_name": "Linke",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#CD3E72",
                        "border_color": None,
                    },
                },
            }
        ]

        for item in test_responses:
            check_response = False
            for response_item in response.json():
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
        response = client.get("/v1/search?text=55278")
        assert response.status_code == 200
        assert type(response.json()) is list
        test_responses = [
            {"id": 177457, "label": "Chiara Pohl"},
            {"id": 175546, "label": "Christian Engelke"},
            {"id": 176888, "label": "David Hess"},
        ]

        for item in test_responses:
            check_response = False
            for response_item in response.json():
                if (
                    item["id"] == response_item["id"]
                    and item["label"] == response_item["label"]
                ):
                    check_response = True
                    break
            assert check_response, "{} item not fount in the response".format(item)

    def test_response_size():
        response = client.get("/v1/search?text=Christian")
        assert len(response.json()) <= 20

    selected_values_test()
    test_response_size()


def test_read_politician_votes():
    def no_filters_random_test():
        response = client.get("/v1/politician/79137/votes")
        test_responses = [
            {
                "Vote": {
                    "id": 418919,
                    "entity_type": "vote",
                    "label": "Angela Merkel - Einsatz deutscher Streitkräfte zur militärischen Evakuierung aus Afghanistan",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/418919",
                    "mandate_id": 44550,
                    "fraction_id": 81,
                    "poll_id": 4283,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4283,
                    "label": "Einsatz deutscher Streitkräfte zur militärischen Evakuierung aus Afghanistan",
                    "field_intro": '<p>Der von der Bundesregierung eingebrachte <a class="link-download" href="https://dserver.bundestag.de/btd/19/320/1932022.pdf">Antrag</a> sieht vor, dass der Bundestag rückwirkend der Entsendung von deutschen Streitkräften nach Afghanistan zustimmt. Diese Entscheidung wurde bereits am 15. August durch den Krisenstab der Bundesregierung getroffen. Angesichts der sich dramatisch verschlechterten Sicherheitslage in Afghanistan soll die militärische Evakuierung fortgesetzt werden.</p>\r\n\r\n<p>Der Antrag wurde mit 538 Ja-Stimmen aus den Reihen aller Fraktionen <strong>angenommen</strong>. Neun Abgeordnete, insbesondere aus der Fraktion Die LINKE, stimmten gegen den Antrag. Dabei enthielten sich 89 Abgeordnete der AfD- und Die LINKE-Fraktion.</p>\r\n',
                    "field_poll_date": "2021-08-25",
                    "poll_passed": True,
                },
            },
        ]

        for item in test_responses:
            assert item in response.json()["items"]

    def response_size_by_filters_test():
        complete_response_total = client.get("/v1/politician/119742/votes").json()[
            "total"
        ]
        single_filter_response_total = client.get(
            "/v1/politician/119742/votes?filters=2"
        ).json()["total"]
        double_filter_response_total = client.get(
            "/v1/politician/119742/votes?filters=2&filters=1"
        ).json()["total"]
        triple_filter_response_total = client.get(
            "/v1/politician/119742/votes?filters=2&filters=1&filters=6"
        ).json()["total"]

        assert complete_response_total >= triple_filter_response_total
        assert triple_filter_response_total >= double_filter_response_total
        assert double_filter_response_total >= single_filter_response_total

    no_filters_random_test()
    response_size_by_filters_test()


def test_read_poll_details():
    def random_test():
        response = client.get("/v1/poll/4217/details")
        assert response.status_code == 200
        # maybe shift out into another file
        response_items = {
            "poll_results": [
                {
                    "id": 421714,
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
                    "id": 4217153,
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
            ],
            "poll_links": [
                {
                    "uri": "https://dserver.bundestag.de/btd/19/281/1928173.pdf",
                    "title": "Gesetzentwurf",
                },
                {
                    "uri": "https://dserver.bundestag.de/btd/19/309/1930938.pdf",
                    "title": "Beschlussempfehlung",
                },
                {
                    "uri": "https://dserver.bundestag.de/btd/19/311/1931118.pdf",
                    "title": "Bericht",
                },
                {
                    "uri": "https://dserver.bundestag.de/btd/19/281/1928173.pdf",
                    "title": "Gesetzentwurf",
                },
                {
                    "uri": "https://dserver.bundestag.de/btd/19/309/1930938.pdf",
                    "title": "Beschlussempfehlung",
                },
                {
                    "uri": "https://dserver.bundestag.de/btd/19/311/1931118.pdf",
                    "title": "Bericht",
                },
            ],
        }
        for item in response_items:
            assert item in response.json()

    def test_unique_fractions_in_response():
        response = client.get("/v1/poll/4174/details")
        fraction_ids = []
        for item in response.json()["poll_results"]:
            fraction_id = item["fraction"]["id"]
            assert (
                fraction_id not in fraction_ids
            ), f"duplicate fraction of id {fraction_id} in response. All objects must have a unique fraction id"
            fraction_ids.append(fraction_id)

    def test_same_poll_id_in_response():
        poll_id = 713
        response = client.get(f"/v1/poll/{poll_id}/details")

        for item in response.json()["poll_results"]:
            assert (
                item["poll_id"] == poll_id
            ), f"Item of id {item['id']} is returned with poll_id {item['poll_id']}. Only items with poll_id {poll_id} should be returned"

    random_test()
    test_unique_fractions_in_response()
    test_same_poll_id_in_response()


def test_read_politician_speech():
    def selected_values_test():
        response = client.get("/v1/politician/119742/speeches?page=6")
        response_items = [
            {
                "videoFileURI": "https://cldf-od.r53.cdn.tv1.eu/1000153copo/ondemand/app144277506/145293313/7193961/7193961_h264_720_400_2000kb_baseline_de_2192.mp4",
                "title": "55 Jahre Élysée-Vertrag",
                "date": "2018-01-22T10:50:46",
            }
        ]

        for item in response_items:
            assert item in response.json()["items"]
        assert response.json()["is_last_page"] is True

    def selected_invalid_values_test():
        response = client.get("/v1/politician/119742/speeches?page=7")
        expected = {
            "items": [],
            "total": 0,
            "page": 7,
            "size": 0,
            "is_last_page": True,
            "politician_id": 119742,
        }
        assert response.json() == expected

    selected_values_test()
    selected_invalid_values_test()


def test_read_politician_news():
    def values_test():
        response = client.get("/v1/politician/145862/news")
        # maybe shift out into another file
        expected_items = {
            "items": [
                {
                    "id": "7440c00ed39a1cdd627a7c461097595ead732077f2758e75525e60ba772d5268",
                    "highlight": None,
                    "images": [
                        {
                            "url": "https://cdn.prod.www.spiegel.de/images/575ebbb2-44c1-4d8b-9e70-706143112610_w1200_r1.77_fpx64.47_fpy50.jpg",
                            "title": None,
                            "height": None,
                            "width": None,
                        },
                        {
                            "url": "https://cdn.prod.www.spiegel.de/images/575ebbb2-44c1-4d8b-9e70-706143112610_w1200_r1.33_fpx64.47_fpy50.jpg",
                            "title": None,
                            "height": None,
                            "width": None,
                        },
                        {
                            "url": "https://cdn.prod.www.spiegel.de/images/575ebbb2-44c1-4d8b-9e70-706143112610_w1200_r1_fpx64.47_fpy50.jpg",
                            "title": None,
                            "height": None,
                            "width": None,
                        },
                    ],
                    "published": "2022-04-14T14:39:53",
                    "source": "spon",
                    "title": "Nord Stream 2: CDU-Politiker Amthor stellt Schwesigs Glaubwürdigkeit infrage",
                    "url": "https://www.spiegel.de/politik/deutschland/nord-stream-2-philipp-amthor-stellt-glaubwuerdigkeit-von-manuela-schwesig-infrage-a-2613f78c-1f6f-44dd-a2be-014fa0df115d",
                },
                {
                    "id": "43fbcd326136b5e5d7374ab3881ae88249945d1d97a2de4b993a286b04196bf5",
                    "highlight": None,
                    "images": [
                        {
                            "url": "https://bilder.bild.de/fotos-skaliert/am-tag-nach-dem-koalitionsvertrag-erste-ampel-stoerung-wegen-impfpflicht-77b296b930664a44953c94a849a40595-78348716/11,c=0,h=720.bild.jpg",
                            "title": None,
                            "height": 720,
                            "width": 1280,
                        },
                        {
                            "url": "https://bilder.bild.de/fotos-skaliert/am-tag-nach-dem-koalitionsvertrag-erste-ampel-stoerung-wegen-impfpflicht-77b296b930664a44953c94a849a40595-78348750/11,c=0,h=658.bild.jpg",
                            "title": None,
                            "height": 658,
                            "width": 658,
                        },
                        {
                            "url": "https://bilder.bild.de/fotos-skaliert/am-tag-nach-dem-koalitionsvertrag-erste-ampel-stoerung-wegen-impfpflicht-77b296b930664a44953c94a849a40595-78348758/11,c=0,h=1026.bild.jpg",
                            "title": None,
                            "height": 1026,
                            "width": 864,
                        },
                    ],
                    "published": "2021-11-25T12:21:10",
                    "source": "bild",
                    "title": "Am Tag nach dem Koalitionsvertrag: Erste Ampel-Störung wegen Impfpflicht",
                    "url": "https://www.bild.de/politik/inland/politik-inland/am-tag-nach-dem-koalitionsvertrag-erste-ampel-stoerung-wegen-impfpflicht-78347556.bild.html",
                },
                {
                    "id": "0fa2f128e7540a5c5d2d3aaea91b340967a5bdb1db3a41bb1774bd70b0db7671",
                    "highlight": None,
                    "images": [],
                    "published": "2021-11-24T13:21:29",
                    "source": "welt",
                    "title": "Philipp Amthor muss seinen Führerschein abgeben",
                    "url": "https://www.welt.de/politik/deutschland/article235256256/Philipp-Amthor-muss-seinen-Fuehrerschein-abgeben.html",
                },
                {
                    "id": "04447aa6e5f9219722acc693b5e58737e3d66e1876aae991150f3b5f5c46a27b",
                    "highlight": None,
                    "images": [],
                    "published": "2021-11-17T08:11:00",
                    "source": "welt",
                    "title": "Philipp Amthor: 50 km/h zu schnell – CDU-Politiker soll Führerschein abgeben",
                    "url": "https://www.welt.de/politik/deutschland/article235100096/Philipp-Amthor-50-km-h-zu-schnell-CDU-Politiker-soll-Fuehrerschein-abgeben.html",
                },
            ],
            "total": 100,
            "page": 1,
            "size": 50,
        }

        for item in expected_items["items"]:
            assert item in response.json()["items"]

    def wrong_input_test():
        response = client.get("/v1/politician/z/news")
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["path", "id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }

    wrong_input_test()
    values_test()


def test_read_bundestag_sidejobs():
    def values_test():
        response_items = client.get("/v1/bundestag/sidejobs")
        assert response_items.status_code == 200
        assert type(response_items.json()) is list
        assert len(response_items.json()) == 5
        for item in response_items.json():
            assert "sidejob" in item
            assert "politician" in item

    values_test()


def test_read_bundestag_sidejobs_pagination():
    def values_test():
        response = client.get("v1/bundestag/allsidejobs?page=1&size=50")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert len(response.json()["items"]) == 50
        assert response.json()["size"] == 50
        assert response.json()["page"] == 1
        for item in response.json()["items"]:
            assert "sidejob" in item
            assert "politician" in item

    def selected_values_test():
        response = client.get("v1/bundestag/allsidejobs?page=1&size=50")
        response_item = {
            "sidejob": {
                "id": 11700,
                "entity_type": "sidejob",
                "label": "Mitglied des Kreistages, ehrenamtlich",
                "income_level": None,
                "interval": None,
                "created": "2021-11-29",
                "sidejob_organization": {
                    "id": 1791,
                    "entity_type": "sidejob_organization",
                    "label": "Landkreis Uckermark",
                },
            },
            "politician": {
                "id": 78902,
                "label": "Stefan Zierke",
                "party": {
                    "id": 1,
                    "label": "SPD",
                    "party_style": {
                        "id": 1,
                        "display_name": "SPD",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#E95050",
                        "border_color": None,
                    },
                },
            },
        }

        assert response_item in response.json()["items"]

    def selected_invalid_values_test():
        response = client.get("v1/bundestag/allsidejobs?page=22&size=50")
        response_items = []
        assert response.json()["items"] == response_items

    values_test()
    selected_values_test()
    selected_invalid_values_test()


def test_read_homepage_party_donations():
    response = client.get("/v1/homepagepartydonations")
    response_json = response.json()
    assert response.status_code == 200

    assert len(response_json) == 8  # only true while parties are hardcoded

    # not covered by schema
    for party in response_json:
        assert len(party["donations_over_96_months"]) == 96
        assert sum(party["donations_over_96_months"]) == party["donations_total"]

    # add test for id not found
