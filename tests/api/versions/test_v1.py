from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

#### GENERAL NOTES ####

# Potential things to consider:
# status of entity (retired/active, will fields change? consider mocking)
# size of lists/dicts (what are the default boundaries? 0-what?)
# testing variations of the parameters (e.g. for start/end size or paginations)
# testing negatives (missing resource)
# testing missing routes: politicianshistory, poll/id/votes, bundestag/speeches, bundestag/polls, bundestag/allpolls, partydonations
# split tests out into single methods instead of larger ones (otherwise a single failure blocks the whole test)
# add human-readable error messages

# test_politician_votes_route_expected_values
# test_politician_votes_route_parameters
# test_politician_votes_route_does_not_exist
# test_politician_votes_route_invalid_parameter

# test_poll_details_route_expected_values
# test_poll_details_route_does_not_exist

# Tests politician route for single ID with default parameters (6 most recent votes and polls) for deceased politican (no updates)
def test_politician_route_expected_values():
    response = client.get("/v1/politician/28881")
    assert response.status_code == 200

    assert response.json() == {
        "id": 28881,
        "label": "Martina Michels",
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
        "occupations": ["MdEP"],
        "sidejobs": [],
        "cvs": [],
        "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/martina-michels",
        "weblinks": [
            {
                "politician_id": 28881,
                "id": 46665,
                "link": "https://www.martina-michels.de/",
            },
            {
                "politician_id": 28881,
                "id": 46666,
                "link": "https://twitter.com/martina_michels",
            },
            {
                "politician_id": 28881,
                "id": 46667,
                "link": "https://www.facebook.com/martina.michels.549",
            },
            {
                "politician_id": 28881,
                "id": 46668,
                "link": "https://www.dielinke-europa.eu/",
            },
        ],
        "votes_and_polls": [
            {
                "Vote": {
                    "id": 468432,
                    "entity_type": "vote",
                    "label": "Martina Michels - Einheitliche Ladekabel mit USB-C ab 2024",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/468432",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4795,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4795,
                    "label": "Einheitliche Ladekabel mit USB-C ab 2024",
                    "field_intro": '<p>Das Europäische Parlament hat am 04. Oktober 2022 namentlich über einen <a class="link-read-more" href="https://www.europarl.europa.eu/doceo/document/A-9-2022-0129_DE.html">Vorschlag </a>der EU-Kommission für eine Richtlinie zur Vereinheitlichung von Ladegeräten mit USB-C abgestimmt. Ab Mitte 2024 sollen kleinere elektronische Geräte nur noch mit USB-C-Anschluss verkauft werden. Für Drucker, Mäuse und Laptops gilt diese Vorgabe ab 2026.</p>\r\n\r\n<p>Der Kommissionsvorschlag wurde nahezu einheitlich angenommen, nur 13 Abgeordnete stimmten dagegen. Somit bleiben den nationalen Parlamenten zwei Jahre, um die Richtlinie in nationales Recht umzusetzen.</p>\r\n\r\n<p>Von den deutschen Abgeordneten stimmten 85 dafür und niemand dagegen. Enthalten hat sich ein Abgeordneter.</p>\r\n',
                    "field_poll_date": "2022-10-04",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 471512,
                    "entity_type": "vote",
                    "label": "Martina Michels - Angemessener Mindestlohn in der EU",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/471512",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4800,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4800,
                    "label": "Angemessener Mindestlohn in der EU",
                    "field_intro": '<p>Das Europäische Parlament hat am 14. September 2022 namentlich über einen <a class="link-read-more" href="https://www.europarl.europa.eu/doceo/document/TA-9-2022-0316_DE.html">Gesetzentwurf </a>zur Einführung eines angemessenen Mindestlohns in allen Mitgliedstaaten abgestimmt. Die EU strebt damit an, die soziale Gerechtigkeit und die Gleichstellung von Frauen und Männern sowie den Erhalt eines hohen Beschäftigungsniveaus zu fördern.</p>\r\n\r\n<p>Der Gesetzentwurf wurde mit 505 Stimmen <strong>angenommen</strong>. 92 Abgeordnete stimmten dagegen und 44 Abgeordnete enthielten sich. Von den deutschen Abgeordneten stimmten insgesamt 73 für den Gesetzesentwurf und zehn dagegen.</p>\r\n',
                    "field_poll_date": "2022-09-14",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 455074,
                    "entity_type": "vote",
                    "label": "Martina Michels - Keine Einstufung von Erdgas und Atomkraft als nachhaltig",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/455074",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4662,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4662,
                    "label": "Keine Einstufung von Erdgas und Atomkraft als nachhaltig",
                    "field_intro": '<p>Mit dem vorgelegten <a class="link-read-more" href="https://www.europarl.europa.eu/doceo/document/B-9-2022-0338_DE.pdf">Entschließungsantrag </a>des Europäischen Parlaments sollte das Vorhaben der Delegierten Verordnung der Kommission verhindert werden, die Taxonomie dahingehend zu ändern, dass zukünftig Investitionen in Erdgas und Atomkraft als nachhaltig eingestuft werden könnten.</p>\r\n\r\n<p>Für den Entschließungsantrag stimmten 278 EU-Abgeordnete - um das Vorhaben zu blockieren, wären 353 Zustimmungen notwendig gewesen. 328 Abgeordnete stimmten gegen den Antrag, 33 enthielten sich.</p>\r\n\r\n<p>Von den 96 deutschen Abgeordneten stimmten 59 Abgeordnete dafür, 21 dagegen und sieben enthielten sich. Die Mehrheit der deutschen EU-Abgeordneten stimmte demnach gegen die Änderungen der Taxonomie.</p>\r\n',
                    "field_poll_date": "2022-07-06",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 443836,
                    "entity_type": "vote",
                    "label": "Martina Michels - Entschluss über eine Wahlreform für die EU-Parlamentswahlen",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/443836",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4598,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4598,
                    "label": "Entschluss über eine Wahlreform für die EU-Parlamentswahlen",
                    "field_intro": '<p>Das Europäische Parlament hat über einen <a href="https://www.europarl.europa.eu/doceo/document/A-9-2022-0083_DE.html">Entschließungsantrag</a> zur Wahlreform abgestimmt. Dieser beinhaltet eine Sperrklausel von 3,5 Prozent für die Parteien bei der nächsten EU-Parlamentswahl. Außerdem sollen national übergreifende Listenkandidierende aufgestellt werden und der Wahltag einheitlich auf den 9. Mai festgelegt werden.</p>\r\n\r\n<p>Von den 96 deutschen Mitgliedern des EU-Parlamentes haben<strong> 70 für den Entschluss und 12 dagegen gestimmt</strong>. Es gab sechs Enthaltungen, acht Abgeordnete haben sich nicht an der Abstimmung beteiligt</p>\r\n',
                    "field_poll_date": "2022-05-03",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 436368,
                    "entity_type": "vote",
                    "label": "Martina Michels - EU-Richtlinie zur Lohntransparenz",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/436368",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4566,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4566,
                    "label": "EU-Richtlinie zur Lohntransparenz",
                    "field_intro": '<p>Das EU-Parlament hat eine <a class="link-read-more" href="https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:52021PC0093&amp;qid=1651063385803&amp;from=EN">Richtlinie des EU-Parlamentes und des Rates</a> mehrheitlich beschlossen. Die Richtlinie "zur Stärkung der Anwendung des Grundsatzes des gleichen Entgeltes für Männer und Frauen bei gleicher oder gleichwertiger Arbeit (...)" knüpft an bereits geltende Richtlinien an. Hintergrund sei die weiterhin herausfordernde Umsetzung der Lohntransparenz und damit einhergehende Unterschiede zwischen dem Gehalt von Männern und Frauen bei gleicher Arbeit.</p>\r\n\r\n<p>Von den 96 deutschen Mitgliedern des EU-Parlamentes haben 51 für die Richtlinie und 37 dagegen gestimmt. Es gab sechs Enthaltungen, zwei Abgeordnete haben sich nicht an der Abstimmung beteiligt.</p>\r\n',
                    "field_poll_date": "2022-04-05",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 436303,
                    "entity_type": "vote",
                    "label": "Martina Michels - Abwehr von ausländischen Einflüssen auf demokratische Prozesse in der EU",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/436303",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4562,
                    "vote": "abstain",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4562,
                    "label": "Abwehr von ausländischen Einflüssen auf demokratische Prozesse in der EU",
                    "field_intro": '<p>Das EU-Parlament hat mit großer Mehrheit einen <a class="link-download" href="https://www.europarl.europa.eu/doceo/document/A-9-2022-0022_EN.html">Bericht</a> der lettischen Abgeordneten Sandra Kalniete angenommen, der unterschiedliche Vorhaben zur Stärkung der europäischen Demokratie gegen ausländische Einflüsse vorschlägt. Der Bericht konzentriert sich dabei insbesondere auf Einflussnahmen durch Russland und China.</p>\r\n\r\n<p>Von den 96 deutschen Europaabgeordneten stimmten 79 dafür. Zwölf Abgeordnete, vor allem aus den Reihen der AfD, stimmten gegen den Bericht. Vier Abgeordnete haben sich enthalten.</p>\r\n',
                    "field_poll_date": "2022-03-09",
                    "poll_passed": True,
                },
            },
        ],
        "topic_ids_of_latest_committee": [3, 7, 12, 18],
    }


# Tests politician route for single ID for which there is no matching politician
def test_politician_route_does_not_exist():
    response = client.get("/v1/politician/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politician not found"}


# Tests politician route for single ID with modified parameters (votes_start, end_start, combination)
def test_politician_route_modified_parameters():
    # response = client.get("/v1/politician/78973?votes_start=4")
    # assert response.json() == v1_expected_responses.politician_route_modified_votes_start_parameter

    # Should return 8 most recent votes and polls, ordered most recent to oldest
    response = client.get("/v1/politician/28881?votes_end=8")
    assert response.json() == {
        "id": 28881,
        "label": "Martina Michels",
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
        "occupations": ["MdEP"],
        "sidejobs": [],
        "cvs": [],
        "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/martina-michels",
        "weblinks": [
            {
                "link": "https://www.martina-michels.de/",
                "id": 46665,
                "politician_id": 28881,
            },
            {
                "link": "https://twitter.com/martina_michels",
                "id": 46666,
                "politician_id": 28881,
            },
            {
                "link": "https://www.facebook.com/martina.michels.549",
                "id": 46667,
                "politician_id": 28881,
            },
            {
                "link": "https://www.dielinke-europa.eu/",
                "id": 46668,
                "politician_id": 28881,
            },
        ],
        "votes_and_polls": [
            {
                "Vote": {
                    "id": 468432,
                    "entity_type": "vote",
                    "label": "Martina Michels - Einheitliche Ladekabel mit USB-C ab 2024",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/468432",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4795,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4795,
                    "label": "Einheitliche Ladekabel mit USB-C ab 2024",
                    "field_intro": '<p>Das Europäische Parlament hat am 04. Oktober 2022 namentlich über einen <a class="link-read-more" href="https://www.europarl.europa.eu/doceo/document/A-9-2022-0129_DE.html">Vorschlag </a>der EU-Kommission für eine Richtlinie zur Vereinheitlichung von Ladegeräten mit USB-C abgestimmt. Ab Mitte 2024 sollen kleinere elektronische Geräte nur noch mit USB-C-Anschluss verkauft werden. Für Drucker, Mäuse und Laptops gilt diese Vorgabe ab 2026.</p>\r\n\r\n<p>Der Kommissionsvorschlag wurde nahezu einheitlich angenommen, nur 13 Abgeordnete stimmten dagegen. Somit bleiben den nationalen Parlamenten zwei Jahre, um die Richtlinie in nationales Recht umzusetzen.</p>\r\n\r\n<p>Von den deutschen Abgeordneten stimmten 85 dafür und niemand dagegen. Enthalten hat sich ein Abgeordneter.</p>\r\n',
                    "field_poll_date": "2022-10-04",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 471512,
                    "entity_type": "vote",
                    "label": "Martina Michels - Angemessener Mindestlohn in der EU",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/471512",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4800,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4800,
                    "label": "Angemessener Mindestlohn in der EU",
                    "field_intro": '<p>Das Europäische Parlament hat am 14. September 2022 namentlich über einen <a class="link-read-more" href="https://www.europarl.europa.eu/doceo/document/TA-9-2022-0316_DE.html">Gesetzentwurf </a>zur Einführung eines angemessenen Mindestlohns in allen Mitgliedstaaten abgestimmt. Die EU strebt damit an, die soziale Gerechtigkeit und die Gleichstellung von Frauen und Männern sowie den Erhalt eines hohen Beschäftigungsniveaus zu fördern.</p>\r\n\r\n<p>Der Gesetzentwurf wurde mit 505 Stimmen <strong>angenommen</strong>. 92 Abgeordnete stimmten dagegen und 44 Abgeordnete enthielten sich. Von den deutschen Abgeordneten stimmten insgesamt 73 für den Gesetzesentwurf und zehn dagegen.</p>\r\n',
                    "field_poll_date": "2022-09-14",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 455074,
                    "entity_type": "vote",
                    "label": "Martina Michels - Keine Einstufung von Erdgas und Atomkraft als nachhaltig",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/455074",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4662,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4662,
                    "label": "Keine Einstufung von Erdgas und Atomkraft als nachhaltig",
                    "field_intro": '<p>Mit dem vorgelegten <a class="link-read-more" href="https://www.europarl.europa.eu/doceo/document/B-9-2022-0338_DE.pdf">Entschließungsantrag </a>des Europäischen Parlaments sollte das Vorhaben der Delegierten Verordnung der Kommission verhindert werden, die Taxonomie dahingehend zu ändern, dass zukünftig Investitionen in Erdgas und Atomkraft als nachhaltig eingestuft werden könnten.</p>\r\n\r\n<p>Für den Entschließungsantrag stimmten 278 EU-Abgeordnete - um das Vorhaben zu blockieren, wären 353 Zustimmungen notwendig gewesen. 328 Abgeordnete stimmten gegen den Antrag, 33 enthielten sich.</p>\r\n\r\n<p>Von den 96 deutschen Abgeordneten stimmten 59 Abgeordnete dafür, 21 dagegen und sieben enthielten sich. Die Mehrheit der deutschen EU-Abgeordneten stimmte demnach gegen die Änderungen der Taxonomie.</p>\r\n',
                    "field_poll_date": "2022-07-06",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 443836,
                    "entity_type": "vote",
                    "label": "Martina Michels - Entschluss über eine Wahlreform für die EU-Parlamentswahlen",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/443836",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4598,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4598,
                    "label": "Entschluss über eine Wahlreform für die EU-Parlamentswahlen",
                    "field_intro": '<p>Das Europäische Parlament hat über einen <a href="https://www.europarl.europa.eu/doceo/document/A-9-2022-0083_DE.html">Entschließungsantrag</a> zur Wahlreform abgestimmt. Dieser beinhaltet eine Sperrklausel von 3,5 Prozent für die Parteien bei der nächsten EU-Parlamentswahl. Außerdem sollen national übergreifende Listenkandidierende aufgestellt werden und der Wahltag einheitlich auf den 9. Mai festgelegt werden.</p>\r\n\r\n<p>Von den 96 deutschen Mitgliedern des EU-Parlamentes haben<strong> 70 für den Entschluss und 12 dagegen gestimmt</strong>. Es gab sechs Enthaltungen, acht Abgeordnete haben sich nicht an der Abstimmung beteiligt</p>\r\n',
                    "field_poll_date": "2022-05-03",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 436368,
                    "entity_type": "vote",
                    "label": "Martina Michels - EU-Richtlinie zur Lohntransparenz",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/436368",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4566,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4566,
                    "label": "EU-Richtlinie zur Lohntransparenz",
                    "field_intro": '<p>Das EU-Parlament hat eine <a class="link-read-more" href="https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:52021PC0093&amp;qid=1651063385803&amp;from=EN">Richtlinie des EU-Parlamentes und des Rates</a> mehrheitlich beschlossen. Die Richtlinie "zur Stärkung der Anwendung des Grundsatzes des gleichen Entgeltes für Männer und Frauen bei gleicher oder gleichwertiger Arbeit (...)" knüpft an bereits geltende Richtlinien an. Hintergrund sei die weiterhin herausfordernde Umsetzung der Lohntransparenz und damit einhergehende Unterschiede zwischen dem Gehalt von Männern und Frauen bei gleicher Arbeit.</p>\r\n\r\n<p>Von den 96 deutschen Mitgliedern des EU-Parlamentes haben 51 für die Richtlinie und 37 dagegen gestimmt. Es gab sechs Enthaltungen, zwei Abgeordnete haben sich nicht an der Abstimmung beteiligt.</p>\r\n',
                    "field_poll_date": "2022-04-05",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 436303,
                    "entity_type": "vote",
                    "label": "Martina Michels - Abwehr von ausländischen Einflüssen auf demokratische Prozesse in der EU",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/436303",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4562,
                    "vote": "abstain",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4562,
                    "label": "Abwehr von ausländischen Einflüssen auf demokratische Prozesse in der EU",
                    "field_intro": '<p>Das EU-Parlament hat mit großer Mehrheit einen <a class="link-download" href="https://www.europarl.europa.eu/doceo/document/A-9-2022-0022_EN.html">Bericht</a> der lettischen Abgeordneten Sandra Kalniete angenommen, der unterschiedliche Vorhaben zur Stärkung der europäischen Demokratie gegen ausländische Einflüsse vorschlägt. Der Bericht konzentriert sich dabei insbesondere auf Einflussnahmen durch Russland und China.</p>\r\n\r\n<p>Von den 96 deutschen Europaabgeordneten stimmten 79 dafür. Zwölf Abgeordnete, vor allem aus den Reihen der AfD, stimmten gegen den Bericht. Vier Abgeordnete haben sich enthalten.</p>\r\n',
                    "field_poll_date": "2022-03-09",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 420767,
                    "entity_type": "vote",
                    "label": "Martina Michels - Einrichtung einer unabhängigen Ethikbehörde zur Lobbykontrolle von EU-Institutionen",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/420767",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4305,
                    "vote": "yes",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4305,
                    "label": "Einrichtung einer unabhängigen Ethikbehörde zur Lobbykontrolle von EU-Institutionen",
                    "field_intro": '<p>Das EU-Parlament hat einen <a class="link-download" href="https://www.europarl.europa.eu/doceo/document/A-9-2021-0260_DE.html">Bericht</a> des deutschen Grünen-Abgeordneten <a class="link-profile" href="https://www.abgeordnetenwatch.de/profile/daniel-freund">Daniel Freund</a> mit großer Mehrheit angenommen, der die EU-Kommission dazu auffordert, Interessenskonflikte und Korruption in EU-Institutionen in Zukunft von einem unabhängigen Gremium überwachen zu lassen. Bislang hatten die einzelnen Institutionen der EU-Verwaltung selbst kontrolliert, ob bei ihnen die Lobby- und Ethikregeln eingehalten werden.</p>\r\n\r\n<p>Von den 96 deutschen Europaabgeordneten stimmten 50 dafür. Die Abgeordneten der CDU/CSU enthielten sich bei der Abstimmung, die der AfD stimmten gegen den Entwurf.</p>\r\n',
                    "field_poll_date": "2021-09-16",
                    "poll_passed": True,
                },
            },
            {
                "Vote": {
                    "id": 426118,
                    "entity_type": "vote",
                    "label": "Martina Michels - Sexualisierte Gewalt an Kindern im Internet bekämpfen",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/426118",
                    "mandate_id": 44694,
                    "fraction_id": 251,
                    "poll_id": 4384,
                    "vote": "no",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4384,
                    "label": "Sexualisierte Gewalt an Kindern im Internet bekämpfen",
                    "field_intro": '<p>Mit der namentlichen Abstimmung wurde über den Vorschlag für eine <a class="link-read-more" href="https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A52020PC0568">Verordnung </a>abgestimmt, welche bestimmte Aspekte der <a class="link-read-more" href="https://eur-lex.europa.eu/legal-content/DE/ALL/?uri=celex%3A32002L0058">Richtlinie 2002/58/EG</a> des Europäischen Parlaments (Datenschutzrichtlinie für elektronische Kommunikation) zeitweise aussetzen möchte, um sexualisierte Gewalt an Kindern im Internet zu bekämpfen. Strafrechtlich ist der Tatbestand unter dem Begriff des sexuellen Missbrauchs bekannt.</p>\r\n\r\n<p>Von den deutschen EU-Abgeordneten stimmten hauptsächlich CDU/CSU-Abgeordnete und einige SPD-Abgeordnete dafür, dagegen stimmten Abgeordnete aus den Reihen der Bündnis 90/Die Grünen, Die Linke sowie AfD. Auch wenn die deutschen Abgeordneten in der Mehrheit <strong>gegen </strong>die Verordnung stimmten, wurde der Vorschlag über die Verordnung mit insgesamt 537 Stimmen aller EU-Abgeordneten <strong>angenommen.</strong></p>\r\n',
                    "field_poll_date": "2021-07-06",
                    "poll_passed": False,
                },
            },
        ],
        "topic_ids_of_latest_committee": [3, 7, 12, 18],
    }


# Tests politician route for single ID with invalid parameters (negative integers, floats, strings)
# API current uses python indexing for negative integers and a non-user friendly error for floats and strings


def test_politician_route_invalid_parameters():
    response = client.get("/v1/politician/78973?votes_start=-10&votes_end=-2")
    # assert user friendly error message, don't allow negative integers (confirm design)
    response = client.get("/v1/politician/78973?votes_start=.03&votes_end=1.6")
    # assert user friendly error message, don't allow floats
    response = client.get("/v1/politician/78973?votes_start=sandwich&votes_end=banana")
    # assert user friendly error message, don't allow strings


# TODO: find different politician ID to test
def test_politicians_route_expected_values_single_id():
    response = client.get("v1/politicians/?ids=78973")
    assert response.status_code == 200
    # assert response.json() == v1_expected_responses.politicians_route_standard


# TODO: find different politician ID to test
def test_politicians_route_expected_values_multiple_ids():
    response = client.get("/v1/politicians/?ids=78973&ids=78974")
    assert response.status_code == 200
    # assert response.json() == v1_expected_responses.politicians_route_standard


# TODO: find different politician ID to test
def test_politicians_route_single_id_modified_parameters():
    # Currently returns votes 4 through 6 (the default end), should probably return 4 through end of list
    # TODO: confirm design
    response = client.get("/v1/politicians/?ids=78973&?votes_start=4")
    # TODO: add expected response to expected values file
    # assert response.json() == v1_expected_responses

    response = client.get("/v1/politicians/?ids=78973&?votes_end=8")
    # TODO: add expected response to expected values file
    # assert response.json() == v1_expected_responses

    response = client.get("/v1/politicians/?ids=78973&?votes_start=3&votes_end=12")
    # TODO: add expected response to expected values file
    # assert response.json() == v1_expected_responses


# TODO: find different politician ID to test
def test_politicians_route_single_id_invalid_parameters():
    response = client.get("/v1/politicians/78973?votes_start=-10&votes_end=-2")
    # assert user friendly error message, don't allow negative integers (confirm design)
    response = client.get("/v1/politicians/78973?votes_start=.03&votes_end=1.6")
    # assert user friendly error message, don't allow floats
    response = client.get("/v1/politicians/78973?votes_start=sandwich&votes_end=banana")
    # assert user friendly error message, don't allow strings


# TODO: find different politician IDs to test
def test_politicians_route_multiple_ids_modified_parameters():
    # Currently returns votes 4 through 6 (the default end), should probably return 4 through end of list
    # TODO: confirm design
    response = client.get("/v1/politicians/?ids=78973&ids=78974?votes_start=4")
    # TODO: add expected response to expected values file
    # assert response.json() == v1_expected_responses

    response = client.get("/v1/politicians/?ids=78973&ids=78974&?votes_end=8")
    # TODO: add expected response to expected values file
    # assert response.json() == v1_expected_responses

    response = client.get(
        "/v1/politicians/?ids=78973&ids=78974?votes_start=3&votes_end=12"
    )
    # TODO: add expected response to expected values file
    # assert response.json() == v1_expected_responses


# TODO: find different politician IDs to test
def test_politicians_route_multiple_ids_invalid_parameters():
    response = client.get(
        "/v1/politicians/?ids=78973&ids=78974?votes_start=-10&votes_end=-2"
    )
    # assert user friendly error message, don't allow negative integers (confirm design)
    response = client.get(
        "/v1/politicians/?ids=78973&ids=78974?votes_start=.03&votes_end=1.6"
    )
    # assert user friendly error message, don't allow floats
    response = client.get(
        "/v1/politicians/?ids=78973&ids=78974?votes_start=sandwich&votes_end=banana"
    )
    # assert user friendly error message, don't allow strings


# TODO: find different politician IDs to test
def test_politicians_route_does_not_exist_single_id():
    response = client.get("/v1/politicians/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_politicians_route_does_not_exist_multiple_nonexisting_ids():
    response = client.get("/v1/politicians/?ids=1&ids=2")
    assert response.status_code == 404
    # TODO: confirm design (should return "Politicians" or specific error?)
    assert response.json() == {"detail": "Politician not found"}


def test_politicians_route_does_not_exist_duplicate_ids():
    response = client.get("/v1/politicians/?ids=1&ids=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politician not found"}


# TODO: find different politician IDs to test
def test_politicians_route_does_not_exist_multiple_existing_nonexisting_ids():
    response = client.get("/v1/politicians/?ids=1&ids=78973")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politician not found"}


def test_read_politician_constituencies():
    def all_elements_have_values():
        response = client.get("/v1/politician/138540/constituencies")
        assert response.status_code == 200
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

    def None_constituencies_exist():
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
    None_constituencies_exist()


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
            assert check_response, "{} item not found in the response".format(item)

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

    assert len(response_json) == 8  # only True while parties are hardcoded

    # not covered by schema
    for party in response_json:
        assert len(party["donations_over_96_months"]) == 96
        assert sum(party["donations_over_96_months"]) == party["donations_total"]

    # add test for id not found


def test_politicianshistory_route_expected_values_single_id():
    response = client.get("v1/politicianshistory/?ids=78973")
    assert response.json() == [
        {
            "id": 78973,
            "label": "Karin Strenz",
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
        }
    ]


def test_politicianshistory_route_expected_values_multiple_ids():
    response = client.get("v1/politicianshistory/?ids=78973&ids=178584")
    assert response.json() == [
        {
            "id": 78973,
            "label": "Karin Strenz",
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
            "id": 178584,
            "label": "Fadime Tuncer",
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
    ]


def test_politicianshistory_route_does_not_exist_single_id():
    response = client.get("v1/politicianshistory/?ids=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politician not found"}


def test_politicianshistory_route_does_not_exist_multiple_ids():
    response = client.get("v1/politicianshistory/?ids=1&ids=178584")


def test_politicianshistory_route_does_not_exist_duplicate_ids():
    response = client.get("v1/politicianshistory/?ids=78973&ids=78973")
    assert response.json() == [
        {
            "id": 78973,
            "label": "Karin Strenz",
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
        }
    ]


def test_politicianshistory_route_does_not_exist_multiple_existing_nonexisting_ids():
    response = client.get("v1/politicianshistory/?ids=1&ids=178584")
    assert response.json() == {
        "id": 178584,
        "label": "Fadime Tuncer",
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
    }


def test_politician_contituencies_route_expected_values():
    response = client.get("v1/politician/78973/constituencies")
    assert response.json() == {
        "constituency_number": 13,
        "constituency_name": "Ludwigslust-Parchim II - Nordwestmecklenburg II - Landkreis Rostock I",
        "politicians": [
            {
                "id": 79268,
                "label": "Frank Michael Junge",
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
                "id": 78973,
                "label": "Karin Strenz",
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
                "id": 123479,
                "label": "Chris Rehhagen",
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
                "id": 122506,
                "label": "Claudia Schulz",
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
                "id": 123558,
                "label": "Christoph Grimm",
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
                "id": 118757,
                "label": "Horst Krumpen",
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
                "id": 121301,
                "label": "Gustav Graf von Westarp",
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
            {
                "id": 119230,
                "label": "Rainer Schütt",
                "party": {
                    "id": 21,
                    "label": "NPD",
                    "party_style": {
                        "id": 21,
                        "display_name": "NPD",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#9D420F",
                        "border_color": None,
                    },
                },
            },
        ],
    }


def test_politician_contituencies_route_does_not_exist():
    response = client.get("v1/politician/1/constituencies")
    assert response.status_code == 404
    assert response.json() == {"detail": "ConstituencyPolitician not found"}


def test_politician_positions_route_expected_values():
    response = client.get("v1/politician/28881/positions")
    assert response.status_code == 200
    assert response.json() == {"id": 28881, "positions": []}


def test_politician_positions_route_does_not_exist():
    response = client.get("v1/politician/1/positions")
    assert response.status_code == 404
    assert response.json() == {"detail": "Position not found"}


def test_politician_sidejobs_route_expected_values():
    response = client.get("v1/politician/79137/sidejobs?page=1&size=50")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": 1523,
                "entity_type": "sidejob",
                "label": "Mitglied des Ehrensenats",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 1456,
                    "entity_type": "sidejob_organization",
                    "label": "Stiftung Lindauer Nobelpreisträgertreffen am Bodensee",
                },
            },
            {
                "id": 1522,
                "entity_type": "sidejob",
                "label": "Mitglied des Kuratoriums",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 1455,
                    "entity_type": "sidejob_organization",
                    "label": "Stiftung Frauenkirche Dresden",
                },
            },
            {
                "id": 1520,
                "entity_type": "sidejob",
                "label": "Ehrenmitglied des Kuratoriums",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 732,
                    "entity_type": "sidejob_organization",
                    "label": "Stiftung Deutsche Sporthilfe (DSH)",
                },
            },
            {
                "id": 1519,
                "entity_type": "sidejob",
                "label": "Mitglied des Vorstandes",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 249,
                    "entity_type": "sidejob_organization",
                    "label": "Konrad-Adenauer-Stiftung e.V.",
                },
            },
            {
                "id": 1518,
                "entity_type": "sidejob",
                "label": "Ehrenpräsidentin des Kuratoriums",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 1044,
                    "entity_type": "sidejob_organization",
                    "label": "Deutsches Museum",
                },
            },
            {
                "id": 1517,
                "entity_type": "sidejob",
                "label": "Mitglied des Kuratoriums",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 1453,
                    "entity_type": "sidejob_organization",
                    "label": "Deutsche Gesellschaft e.V., Verein zur Förderung politischer, kultureller und sozialer Beziehungen in Europa",
                },
            },
            {
                "id": 1515,
                "entity_type": "sidejob",
                "label": "Vorsitzende des Kuratoriums",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 1022,
                    "entity_type": "sidejob_organization",
                    "label": "Bundesakademie für Sicherheitspolitik (BAKS)",
                },
            },
        ],
        "total": 7,
        "page": 1,
        "size": 50,
    }


def test_politician_sidejobs_route_parameters():
    response = client.get("v1/politician/79137/sidejobs?page=2&size=5")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": 1517,
                "entity_type": "sidejob",
                "label": "Mitglied des Kuratoriums",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 1453,
                    "entity_type": "sidejob_organization",
                    "label": "Deutsche Gesellschaft e.V., Verein zur Förderung politischer, kultureller und sozialer Beziehungen in Europa",
                },
            },
            {
                "id": 1515,
                "entity_type": "sidejob",
                "label": "Vorsitzende des Kuratoriums",
                "income_level": None,
                "interval": None,
                "created": "2017-05-24",
                "sidejob_organization": {
                    "id": 1022,
                    "entity_type": "sidejob_organization",
                    "label": "Bundesakademie für Sicherheitspolitik (BAKS)",
                },
            },
        ],
        "total": 7,
        "page": 2,
        "size": 5,
    }


def test_politician_sidejobs_route_does_not_exist():
    response = client.get("v1/politician/1/sidejobs")
    assert response.status_code == 404
    assert response.json() == {"detail": "Sidejobs not found"}


def test_politician_sidejobs_route_out_of_bounds_parameter():
    response = client.get("v1/politician/79137/sidejobs?page=50&size=1")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 7, "page": 50, "size": 1}


def test_search_route_expected_values():
    response = client.get("v1/search?text=barski")
    assert response.json() == [
        {
            "id": 146712,
            "label": "Daniel Barski",
            "party": {
                "id": 25,
                "label": "Einzelbewerbung",
                "party_style": {
                    "id": 25,
                    "display_name": "Einzelbewerbung",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#333333",
                    "border_color": None,
                },
            },
        },
        {
            "id": 136556,
            "label": "Jürgen Rybarski",
            "party": {
                "id": 115,
                "label": "Die Weissen",
                "party_style": {
                    "id": 115,
                    "display_name": "Die Weissen",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#333333",
                    "border_color": None,
                },
            },
        },
    ]


def test_search_route_does_not_exist():
    response = client.get("v1/search?text=barski")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politicians not found"}


# test_image-scanner_route_expected_values
# test_image-scanner_route_does_not_exist
# test_image-scanner_route_invalid_parameter
