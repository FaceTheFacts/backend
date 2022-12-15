from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

#### GENERAL NOTES ####

# Potential things to consider:
# status of entity (retired/active, will fields change? consider mocking)
# size of lists/dicts (what are the default boundaries? 0-what?)
# testing variations of the parameters (e.g. for start/end size or paginations)
# testing negatives (missing resources)
# split tests out into single methods instead of larger ones (otherwise a single failure blocks the whole test)

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
    # TODO: move to v2 tests (not implemented yet)
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
# TODO: move to v2 tests
# def test_politician_route_invalid_parameters():
#     response = client.get("/v1/politician/78973?votes_start=-10&votes_end=-2")
#     # assert user friendly error message, don't allow negative integers (confirm design)
#     response = client.get("/v1/politician/78973?votes_start=.03&votes_end=1.6")
#     # assert user friendly error message, don't allow floats
#     response = client.get("/v1/politician/78973?votes_start=sandwich&votes_end=banana")
#     # assert user friendly error message, don't allow strings


def test_politicians_route_expected_values_single_id():
    response = client.get("v1/politicians/?ids=28882&votes_end=1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 28882,
            "label": "Stefan Evers",
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
            "occupations": ["MdL"],
            "sidejobs": [],
            "cvs": [],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/stefan-evers",
            "weblinks": [],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 421125,
                        "entity_type": "vote",
                        "label": "Stefan Evers - Bekenntnis zum Neutralitätsgebot an öffentlichen Schulen",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/421125",
                        "mandate_id": 44813,
                        "fraction_id": 156,
                        "poll_id": 4362,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4362,
                        "label": "Bekenntnis zum Neutralitätsgebot an öffentlichen Schulen",
                        "field_intro": '<p>Das Berliner Abgeordnetenhaus stimmte über einen <a class="link-download" href="https://www.parlament-berlin.de/ados/18/IIIPlen/vorgang/d18-0154-1.pdf">Änderungsantrag</a> der CDU-Fraktion ab, der sich für einen Erhalt des Berliner Neutralitätsgesetzes ausspricht. Damit soll verhindert werden, dass Lehrer:innen an öffentlichen Berliner Schulen Kopftuch oder andere sichtbare religiöse Symbole tragen dürfen.</p>\r\n\r\n<p>Der Antrag wurde mit 55 Ja-Stimmen der CDU-, FDP und AfD-Fraktion bei 88 Gegenstimmen der SPD-, Grünen- und Linke-Fraktion <strong>abgelehnt</strong>. Zwei Abgeordnete der Fraktion DIE LINKE haben sich enthalten.</p>\r\n',
                        "field_poll_date": "2021-09-16",
                        "poll_passed": False,
                    },
                }
            ],
            "topic_ids_of_latest_committee": [2, 16, 18],
        }
    ]


def test_politicians_route_expected_values_multiple_ids():
    response = client.get("v1/politicians/?ids=28882&ids=28890&votes_end=1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 28882,
            "label": "Stefan Evers",
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
            "occupations": ["MdL"],
            "sidejobs": [],
            "cvs": [],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/stefan-evers",
            "weblinks": [],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 421125,
                        "entity_type": "vote",
                        "label": "Stefan Evers - Bekenntnis zum Neutralitätsgebot an öffentlichen Schulen",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/421125",
                        "mandate_id": 44813,
                        "fraction_id": 156,
                        "poll_id": 4362,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4362,
                        "label": "Bekenntnis zum Neutralitätsgebot an öffentlichen Schulen",
                        "field_intro": '<p>Das Berliner Abgeordnetenhaus stimmte über einen <a class="link-download" href="https://www.parlament-berlin.de/ados/18/IIIPlen/vorgang/d18-0154-1.pdf">Änderungsantrag</a> der CDU-Fraktion ab, der sich für einen Erhalt des Berliner Neutralitätsgesetzes ausspricht. Damit soll verhindert werden, dass Lehrer:innen an öffentlichen Berliner Schulen Kopftuch oder andere sichtbare religiöse Symbole tragen dürfen.</p>\r\n\r\n<p>Der Antrag wurde mit 55 Ja-Stimmen der CDU-, FDP und AfD-Fraktion bei 88 Gegenstimmen der SPD-, Grünen- und Linke-Fraktion <strong>abgelehnt</strong>. Zwei Abgeordnete der Fraktion DIE LINKE haben sich enthalten.</p>\r\n',
                        "field_poll_date": "2021-09-16",
                        "poll_passed": False,
                    },
                }
            ],
            "topic_ids_of_latest_committee": [2, 16, 18],
        },
        {
            "id": 28890,
            "label": "Daniel Caspary",
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
            "occupations": ["MdEP"],
            "sidejobs": [],
            "cvs": [],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/daniel-caspary",
            "weblinks": [
                {"politician_id": 28890, "id": 46657, "link": "https://caspary.de/"}
            ],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 468387,
                        "entity_type": "vote",
                        "label": "Daniel Caspary - Einheitliche Ladekabel mit USB-C ab 2024",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/468387",
                        "mandate_id": 44650,
                        "fraction_id": 248,
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
                }
            ],
            "topic_ids_of_latest_committee": [11, 19, 21],
        },
    ]


# TODO: move to v2 tests
# def test_politicians_route_single_id_modified_parameters():
#     response = client.get("/v1/politicians/?ids=78973&?votes_start=4")
#     assert response.json() == v1_expected_responses

#     response = client.get("/v1/politicians/?ids=78973&?votes_end=8")
#     assert response.json() == v1_expected_responses

#     response = client.get("/v1/politicians/?ids=78973&?votes_start=3&votes_end=12")
#     assert response.json() == v1_expected_responses

# TODO: move to v2 tests
# def test_politicians_route_single_id_invalid_parameters():
#     response = client.get("/v1/politicians/78973?votes_start=-10&votes_end=-2")
#     assert user friendly error message, don't allow negative integers (confirm design)
#     response = client.get("/v1/politicians/78973?votes_start=.03&votes_end=1.6")
#     assert user friendly error message, don't allow floats
#     response = client.get("/v1/politicians/78973?votes_start=sandwich&votes_end=banana")
#     assert user friendly error message, don't allow strings


def test_politicians_route_multiple_ids_modified_parameters():
    response = client.get("/v1/politicians/?ids=78973&ids=78974?votes_start=4")
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
            "occupations": ["MdB"],
            "sidejobs": [
                {
                    "id": 6893,
                    "entity_type": "sidejob",
                    "label": "Vorsitzende",
                    "income_level": None,
                    "interval": None,
                    "created": "2018-04-16",
                    "sidejob_organization": {
                        "id": 914,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsch-Kasachische Gesellschaft e.V.",
                    },
                },
                {
                    "id": 4541,
                    "entity_type": "sidejob",
                    "label": "Stellv. Vorsitzende, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-09-23",
                    "sidejob_organization": {
                        "id": 914,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsch-Kasachische Gesellschaft e.V.",
                    },
                },
                {
                    "id": 413,
                    "entity_type": "sidejob",
                    "label": "Beteiligung (bis 31.12.2014)",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 872,
                        "entity_type": "sidejob_organization",
                        "label": "Karin Strenz GbR",
                    },
                },
                {
                    "id": 412,
                    "entity_type": "sidejob",
                    "label": "Beratung - Line M-Trade GmbH, Nürnberg (bis Ende Januar 2015)",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 3183,
                        "entity_type": "sidejob_organization",
                        "label": "Beratung - selbständig",
                    },
                },
                {
                    "id": 411,
                    "entity_type": "sidejob",
                    "label": "Beratung - Line M-Trade GmbH, Nürnberg (bis Ende Januar 2015)",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 3183,
                        "entity_type": "sidejob_organization",
                        "label": "Beratung - selbständig",
                    },
                },
            ],
            "cvs": [
                {
                    "id": 633,
                    "short_description": "Geboren am 14. Oktober 1967 in Lübz; evangelisch-lutherisch; verheiratet.",
                    "raw_text": "Besuch der Polytechnischen Oberschule Lübz; Studium am Institut für Lehrerbildung in Rostock; Studium an der Pädagogischen Hochschule in Magdeburg; Abschluss als Diplom-Lehrerin für Sonderschulen; Zusatzstudium der Erziehungswissenschaften an der Goethe-Universität Frankfurt/Main. Lehrerin an der Sonderschule in Wanzleben bei Magdeburg; 1992 bis 2002 Angestellte einer Import- und Großhandelsfirma in Frankfurt/Main. Seit 2015 Vorsitzende der Deutsch-Kasachischen-Gesellschaft e. V. Seit 2001 Vorsitzende des CDU-Kreisverbandes Parchim; 1999 bis 2005 Mitglied des CDU-Landesvorstandes; 2001 bis 2005 Stellvertretende CDU-Landesvorsitzende; Mitglied der Christlich-Demokratische Arbeitnehmerschaft (CDA); seit 2013 Ehrenvorsitzende CDU-Kreisverband Ludwigslust-Parchim. Seit 1999 Mitglied des Kreistages zu Parchim; seit 2001 Vorsitzende der CDU-Kreistagsfraktion Parchim; seit 2002 Mitglied des Landtages von Mecklenburg-Vorpommern; Ausschüsse: Wirtschaft, Arbeit, Bau und Landesentwicklung, Petitionsausschuss; 2002 bis 2006 arbeitsmarktpolitische Sprecherin der CDU-Fraktion; seit November 2007 verantwortlich für das Sorgentelefon der CDU-Fraktion; 2006 bis 2008 Aufsichtsratsvorsitzende des Flughafens Parchim. Mitglied des Deutschen Bundestages seit Oktober 2009. Karin Strenz ist am 21. März 2021 verstorben, Nachfolgerin ist die Abgeordnete Maika Friemann-Jennert, CDU/CSU. ** verstorben ",
                    "politician_id": 78973,
                }
            ],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/karin-strenz",
            "weblinks": [
                {
                    "link": "https://www.wahl.de/politiker/cdu/karin-strenz",
                    "id": 44558,
                    "politician_id": 78973,
                },
                {"link": "http://www.strenz.de/", "id": 44559, "politician_id": 78973},
                {
                    "link": "https://www.wen-waehlen.de/btw09/kandidaten/karin-strenz_10058.html",
                    "id": 44560,
                    "politician_id": 78973,
                },
                {
                    "link": "https://de.wikipedia.org/wiki/Karin_Strenz",
                    "id": 44561,
                    "politician_id": 78973,
                },
                {
                    "link": "https://www.facebook.com/Karin.Strenz",
                    "id": 44562,
                    "politician_id": 78973,
                },
            ],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 364549,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Verlängerung des Bundeswehreinsatzes im Kosovo (KFOR 2020/2021)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/364549",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3711,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3711,
                        "label": "Verlängerung des Bundeswehreinsatzes im Kosovo (KFOR 2020/2021)",
                        "field_intro": '<p>Der von der Bundesregierung eingebrachte <a href="https://dip21.bundestag.de/dip21/btd/19/190/1919001.pdfhttps://dip21.bundestag.de/dip21/btd/19/190/1919003.pdfhttps://dip21.bundestag.de/dip21/btd/19/190/1919002.pdf">Antrag </a>sieht vor, dass die Beteiligung der Bundeswehr an der internationalen Kosovo Force (KFOR) im Kosovo verlängert wird. Bei dem Einsatz handelt es sich um die Unterstützung deutscher Streitkräfte an der Entwicklung eines "stabilen, demokratischen, multiethnischen und friedlichen Kosovos".</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD stimmten der Verlängerung ebenso zu wie die Fraktionen von FDP und Grünen. Damit wurde der Antrag angenommen. AfD und Linke votierten jeweils geschlossen gegen den Antrag.</p>\r\n',
                        "field_poll_date": "2020-06-17",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 363840,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Verlängerung des Bundeswehreinsatzes vor der libanesischen Küste (UNIFIL 2020/2021)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/363840",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3710,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3710,
                        "label": "Verlängerung des Bundeswehreinsatzes vor der libanesischen Küste (UNIFIL 2020/2021)",
                        "field_intro": '<p>Der von der Bundesregierung eingebrachte <a href="https://dip21.bundestag.de/dip21/btd/19/190/1919003.pdfhttps://dip21.bundestag.de/dip21/btd/19/190/1919002.pdf">Antrag </a>sieht vor, dass die Beteiligung der Bundeswehr am maritimen Teil der friedenssichernden Mission "United Nations Interim Force in Lebanon" (<a href="https://www.bundeswehr.de/de/einsaetze-bundeswehr/die-bundeswehr-im-libanon">UNIFIL</a>) verlängert wird. Bei dem Einsatz handelt es sich um die Beteiligung deutscher Streitkräfte an der Überwachung der Seegrenzen des Libanon.</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD stimmten der Verlängerung ebenso zu wie die FDP und die Grünen. Damit wurde der Antrag angenommen. Die AfD-Fraktion und Linke votierten geschlossen gegen den Antrag.</p>\r\n',
                        "field_poll_date": "2020-06-17",
                        "poll_passed": True,
                    },
                },
            ],
            "topic_ids_of_latest_committee": [],
        },
        {
            "id": 78974,
            "label": "Max Straubinger",
            "party": {
                "id": 3,
                "label": "CSU",
                "party_style": {
                    "id": 3,
                    "display_name": "CSU",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#0D6CB4",
                    "border_color": "#F8F8F8",
                },
            },
            "occupations": ["MdB"],
            "sidejobs": [
                {
                    "id": 11680,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2021-09-06",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 11679,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2021-09-06",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9973,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-08-24",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9965,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-08-14",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9768,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Verwaltungsrates, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2020-06-22",
                    "sidejob_organization": {
                        "id": 3796,
                        "entity_type": "sidejob_organization",
                        "label": "DONAUISAR Klinikum Deggendorf-Dingolfing-Landau gKU",
                    },
                },
                {
                    "id": 9176,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "3.500 € bis 7.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9175,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9174,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9173,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9172,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 9171,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 8408,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter (bis 30.09.2019)",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2019-05-21",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 7223,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2018-05-31",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 5841,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 5838,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 5837,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 2951,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Parlamentarischen Beirates",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 370,
                        "entity_type": "sidejob_organization",
                        "label": "Versicherungsombudsmann e.V.",
                    },
                },
                {
                    "id": 2949,
                    "entity_type": "sidejob",
                    "label": "Präsident",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2196,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsches Institut für Reines Bier e.V.",
                    },
                },
                {
                    "id": 2947,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 2946,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Kreistages, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 373,
                        "entity_type": "sidejob_organization",
                        "label": "Landkreis Dingolfing-Landau",
                    },
                },
                {
                    "id": 2944,
                    "entity_type": "sidejob",
                    "label": "Vertreter (bis 30.09.2019)",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 372,
                        "entity_type": "sidejob_organization",
                        "label": "Münchener und Magdeburger Agrarversicherung AG",
                    },
                },
                {
                    "id": 2942,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2941,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "150.000 € bis 250.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2940,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "150.000 € bis 250.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2939,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2938,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "15.000 € bis 30.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2930,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 2926,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 2925,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
            ],
            "cvs": [
                {
                    "id": 571,
                    "short_description": "Geboren am 12. August 1954 in Oberlucken; römisch-katholisch; verheiratet; drei Kinder.",
                    "raw_text": "1973 bis 1974 Grundwehrdienst in München;1970 Gründungsmitglied JU-Ortsverband Simbach; 1985 bis 1989 JU-Kreisvorsitzender Im JU-Kreisverband Dingolfing-Landau;1972 Eintritt in die CSU; 1987 bis 1993 stellvertretender CSU-Kreisvorsitzender; seit 1993 CSU-Kreisvorsitzender im Kreisverband Dingolfing-Landau; 1978 bis 1994 Mitglied des Marktrates von Simbach; seit 1990 Mitglied im Kreistag Dingolfing-Landau MdB; seit 1994 Wahlkreis Rottal-Inn; 2002 bis Dezember 2013 stellvertretender Vorsitzender der CSU-Landesgruppe im Deutschen Bundestag; 2005  bis Dezember 2013 Arbeits- sozial- und gesundheitspolitischer Sprecher der CSU-Landesgruppe im Deutschen Bundestag;  2009  bis Dezember 2013 stellvertretender Vorsitzender des Ausschusses für Arbeit und Soziales im Deutschen Bundestag; 2013 bis 2017 Parlamentarischer Geschäftsführer der CSU-Landesgruppe im Deutschen Bundestag. ",
                    "politician_id": 78974,
                }
            ],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/max-straubinger",
            "weblinks": [
                {
                    "link": "http://www.max-straubinger.de/",
                    "id": 44551,
                    "politician_id": 78974,
                },
                {
                    "link": "https://de.wikipedia.org/wiki/Max_Straubinger",
                    "id": 44552,
                    "politician_id": 78974,
                },
                {
                    "link": "https://www.facebook.com/MaxStraubingerMdB",
                    "id": 44553,
                    "politician_id": 78974,
                },
            ],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 479182,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Inflationsausgleichsgesetz",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/479182",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4831,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4831,
                        "label": "Inflationsausgleichsgesetz",
                        "field_intro": '<p>Der Bundestag stimmte über einen <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/034/2003496.pdf">Gesetzentwurf </a>der Koaltitionsfraktionen ab. Mit dem Inflationsausgleichsgesetz sollen die Effekte der Inflation ausgeglichen werden. Dies soll mit einem angepassten Einkommenssteuertarif und weiteren steuerliche Regelungen errreicht werden.</p>\r\n\r\n<p>Der Gesetzentwurf wurde mit 578 Stimmen von Seiten der Regierungsfraktionen und der Fraktion der CDU/CSU <strong>angenommen</strong>. 35 Abgeordnete der Fraktion Die Linke stimmten gegen den Entwurf. 75 Abgeordnete enthielten sich, darunter die AfD-Fraktion.</p>\r\n',
                        "field_poll_date": "2022-11-10",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 478446,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Einführung des Bürgergeldes",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/478446",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4826,
                        "vote": "no",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4826,
                        "label": "Einführung des Bürgergeldes",
                        "field_intro": '<p>Der <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/038/2003873.pdf">Gesetzentwurf </a>der Bundesregierung fordert die Einführung des sogenannten Bürgergeldes. Der Hartz IV-Nachfolger soll die Grundsicherung für arbeitssuchende Menschen sicherstellen.</p>\r\n\r\n<p>Der Gesetzentwurf wurde mit 385 Stimmen von Seiten der Ampel-Koalition aus SPD, Bündnis 90/Die Grünen und FDP <strong>angenommen</strong>. Die Fraktionen CDU/CSU sowie die AfD stimmten dabei gegen den Gesetzentwurf. Die Abgeordneten der Fraktion Die Linke enthielten sich.</p>\r\n',
                        "field_poll_date": "2022-11-10",
                        "poll_passed": True,
                    },
                },
            ],
            "topic_ids_of_latest_committee": [2, 5, 14, 28],
        },
    ]

    response = client.get("/v1/politicians/?ids=78973&ids=78974&?votes_end=8")
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
            "occupations": ["MdB"],
            "sidejobs": [
                {
                    "id": 6893,
                    "entity_type": "sidejob",
                    "label": "Vorsitzende",
                    "income_level": None,
                    "interval": None,
                    "created": "2018-04-16",
                    "sidejob_organization": {
                        "id": 914,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsch-Kasachische Gesellschaft e.V.",
                    },
                },
                {
                    "id": 4541,
                    "entity_type": "sidejob",
                    "label": "Stellv. Vorsitzende, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-09-23",
                    "sidejob_organization": {
                        "id": 914,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsch-Kasachische Gesellschaft e.V.",
                    },
                },
                {
                    "id": 413,
                    "entity_type": "sidejob",
                    "label": "Beteiligung (bis 31.12.2014)",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 872,
                        "entity_type": "sidejob_organization",
                        "label": "Karin Strenz GbR",
                    },
                },
                {
                    "id": 412,
                    "entity_type": "sidejob",
                    "label": "Beratung - Line M-Trade GmbH, Nürnberg (bis Ende Januar 2015)",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 3183,
                        "entity_type": "sidejob_organization",
                        "label": "Beratung - selbständig",
                    },
                },
                {
                    "id": 411,
                    "entity_type": "sidejob",
                    "label": "Beratung - Line M-Trade GmbH, Nürnberg (bis Ende Januar 2015)",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 3183,
                        "entity_type": "sidejob_organization",
                        "label": "Beratung - selbständig",
                    },
                },
            ],
            "cvs": [
                {
                    "id": 633,
                    "short_description": "Geboren am 14. Oktober 1967 in Lübz; evangelisch-lutherisch; verheiratet.",
                    "politician_id": 78973,
                    "raw_text": "Besuch der Polytechnischen Oberschule Lübz; Studium am Institut für Lehrerbildung in Rostock; Studium an der Pädagogischen Hochschule in Magdeburg; Abschluss als Diplom-Lehrerin für Sonderschulen; Zusatzstudium der Erziehungswissenschaften an der Goethe-Universität Frankfurt/Main. Lehrerin an der Sonderschule in Wanzleben bei Magdeburg; 1992 bis 2002 Angestellte einer Import- und Großhandelsfirma in Frankfurt/Main. Seit 2015 Vorsitzende der Deutsch-Kasachischen-Gesellschaft e. V. Seit 2001 Vorsitzende des CDU-Kreisverbandes Parchim; 1999 bis 2005 Mitglied des CDU-Landesvorstandes; 2001 bis 2005 Stellvertretende CDU-Landesvorsitzende; Mitglied der Christlich-Demokratische Arbeitnehmerschaft (CDA); seit 2013 Ehrenvorsitzende CDU-Kreisverband Ludwigslust-Parchim. Seit 1999 Mitglied des Kreistages zu Parchim; seit 2001 Vorsitzende der CDU-Kreistagsfraktion Parchim; seit 2002 Mitglied des Landtages von Mecklenburg-Vorpommern; Ausschüsse: Wirtschaft, Arbeit, Bau und Landesentwicklung, Petitionsausschuss; 2002 bis 2006 arbeitsmarktpolitische Sprecherin der CDU-Fraktion; seit November 2007 verantwortlich für das Sorgentelefon der CDU-Fraktion; 2006 bis 2008 Aufsichtsratsvorsitzende des Flughafens Parchim. Mitglied des Deutschen Bundestages seit Oktober 2009. Karin Strenz ist am 21. März 2021 verstorben, Nachfolgerin ist die Abgeordnete Maika Friemann-Jennert, CDU/CSU. ** verstorben ",
                }
            ],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/karin-strenz",
            "weblinks": [
                {
                    "link": "https://www.wahl.de/politiker/cdu/karin-strenz",
                    "id": 44558,
                    "politician_id": 78973,
                },
                {"link": "http://www.strenz.de/", "id": 44559, "politician_id": 78973},
                {
                    "link": "https://www.wen-waehlen.de/btw09/kandidaten/karin-strenz_10058.html",
                    "id": 44560,
                    "politician_id": 78973,
                },
                {
                    "link": "https://de.wikipedia.org/wiki/Karin_Strenz",
                    "id": 44561,
                    "politician_id": 78973,
                },
                {
                    "link": "https://www.facebook.com/Karin.Strenz",
                    "id": 44562,
                    "politician_id": 78973,
                },
            ],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 382871,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Internetportal Indymedia verbieten",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/382871",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 4018,
                        "vote": "no",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4018,
                        "label": "Internetportal Indymedia verbieten",
                        "field_intro": '<p>Mit ihrem Antrag fordert die AfD-Fraktion das Verbot des Internetportals <em>indymedia</em>. Laut AfD stelle der Verein eine "Bedrohung der öffentlichen Ordnung durch gewaltbereite Linksextremisten" dar.</p>\r\n\r\n<p>Alle Mitglieder der Fraktionen CDU/CSU, SPD, Grüne. Linke und FDP stimmten ausnahmslos für die Beschlussempfehlung des Ausschusses für Inneres und Heimat und somit gegen den Antrag der AfD.</p>\r\n',
                        "field_poll_date": "2021-02-25",
                        "poll_passed": False,
                    },
                },
                {
                    "Vote": {
                        "id": 373238,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Weiterführung des Bundeswehreinsatzes im Irak",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/373238",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3948,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3948,
                        "label": "Weiterführung des Bundeswehreinsatzes im Irak",
                        "field_intro": '<p>Mit dem Weiterführen des bereits laufenden Bundeswehreinsatzes im Irak soll das erneute Erstarken des islamischen Staates verhindert und die Versöhnung der Konfliktparteien Irak und Syrien gefördert werden.</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD sowie die Fraktion der FDP stimmten der <a href="https://dip21.bundestag.de/dip21/btd/19/232/1923212.pdf">Beschlussempfehlung</a> des Auswärtigen Ausschusses zu. Der Antrag der Bundesregierung wurde somit angenommen. Die Fraktionen Bündnis 90/DieGrünen, Die LINKE und die AfD stimmten einstimmig gegen den Einsatz. Auch neun SPD-Fraktionsmitglieder, darunter <a class="link-profile" href="https://www.abgeordnetenwatch.de/profile/dirk-heidenblut">Dirk Heidenblut</a> und&nbsp;<a class="link-profile" href="https://www.abgeordnetenwatch.de/profile/cansel-kiziltepe">Cansel Kiziltepe</a> stellten sich gegen den den <a href="https://dip21.bundestag.de/dip21/btd/19/222/1922207.pdf">Antrag</a>. Ebenso <a class="link-profile" href="https://www.abgeordnetenwatch.de/profile/wieland-schinnenburg">Dr. Wieland Schinnenburg</a> als einziges Mitglied der Fraktion FDP.</p>\r\n\r\n<p>&nbsp;</p>\r\n',
                        "field_poll_date": "2020-10-29",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 366526,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Nachtragshaushalt 2020: Corona Konjunktur- und Krisenbewältigungspaket",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/366526",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3749,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3749,
                        "label": "Nachtragshaushalt 2020: Corona Konjunktur- und Krisenbewältigungspaket",
                        "field_intro": '<p>Mit dem <a href="http://dip21.bundestag.de/dip21/btd/19/200/1920000.pdf">Gesetzesentwurf </a>fordern die Regierungsfraktionen CDU/CSU und SPD die nachträgliche Erhöhung des Haushaltes für das Jahr 2020 auf 509,3 Milliarden Euro (<a href="https://www.abgeordnetenwatch.de/bundestag/19/abstimmungen/bundeshaushalt-2020">vorher 362 Milliarden Euro</a>) von der Bundesregierung. Mit dem Paket sollen die negativen Auswirkungen auf Wirtschaft und Gesellschaft abgefedert werden.</p>\r\n\r\n<p>Die Regierungsfraktionen stimmten geschlossen <strong>für </strong>den zweiten Nachtragshaushalt. <strong>Gegen </strong>den Antrag votierte die FDP- und AfD-Fraktion. Die Grünen- und Linksfraktion <strong>enthielt </strong>sich zum größten Teil ihrer Stimme. Damit wurde der zweite Nachtragshaushalt für das Jahr 2020 <strong>angenommen</strong>.</p>\r\n',
                        "field_poll_date": "2020-07-02",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 365258,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Umsetzung der EU-Richtlinie: mehr Rechte für Arbeitnehmer:innen aus dem EU-Ausland",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/365258",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3714,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3714,
                        "label": "Umsetzung der EU-Richtlinie: mehr Rechte für Arbeitnehmer:innen aus dem EU-Ausland",
                        "field_intro": '<p>Der <a href="https://dip21.bundestag.de/dip21/btd/19/193/1919371.pdf">Gesetzesentwurf </a>der Bundesregierung will die EU-Richtlinie des EU-Parlamentes zur Stärkung der Rechte von Arbeitnehmer:innen aus dem EU-Ausland umsetzen. Mit der Richtlinie sollen unter anderem aus dem EU-Ausland entsandte Arbeitnehmer:innen nicht mehr nur den Anspruch auf den Mindestlohn, sondern auch auf den Tariflohn aus allgemeinverbindlichen Tarifverträgen haben.</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD stimmten ebenso wie die Grünenfraktion für den Antrag. Dieser wurde damit angenommen. Die AfD stimmte, genau wie die FDP-Fraktion gegen den Antrag. Die Linken-Abgeordneten enthielten sich ihrer Stimme.</p>\r\n',
                        "field_poll_date": "2020-06-18",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 363840,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Verlängerung des Bundeswehreinsatzes vor der libanesischen Küste (UNIFIL 2020/2021)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/363840",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3710,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3710,
                        "label": "Verlängerung des Bundeswehreinsatzes vor der libanesischen Küste (UNIFIL 2020/2021)",
                        "field_intro": '<p>Der von der Bundesregierung eingebrachte <a href="https://dip21.bundestag.de/dip21/btd/19/190/1919003.pdfhttps://dip21.bundestag.de/dip21/btd/19/190/1919002.pdf">Antrag </a>sieht vor, dass die Beteiligung der Bundeswehr am maritimen Teil der friedenssichernden Mission "United Nations Interim Force in Lebanon" (<a href="https://www.bundeswehr.de/de/einsaetze-bundeswehr/die-bundeswehr-im-libanon">UNIFIL</a>) verlängert wird. Bei dem Einsatz handelt es sich um die Beteiligung deutscher Streitkräfte an der Überwachung der Seegrenzen des Libanon.</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD stimmten der Verlängerung ebenso zu wie die FDP und die Grünen. Damit wurde der Antrag angenommen. Die AfD-Fraktion und Linke votierten geschlossen gegen den Antrag.</p>\r\n',
                        "field_poll_date": "2020-06-17",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 364549,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Verlängerung des Bundeswehreinsatzes im Kosovo (KFOR 2020/2021)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/364549",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3711,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3711,
                        "label": "Verlängerung des Bundeswehreinsatzes im Kosovo (KFOR 2020/2021)",
                        "field_intro": '<p>Der von der Bundesregierung eingebrachte <a href="https://dip21.bundestag.de/dip21/btd/19/190/1919001.pdfhttps://dip21.bundestag.de/dip21/btd/19/190/1919003.pdfhttps://dip21.bundestag.de/dip21/btd/19/190/1919002.pdf">Antrag </a>sieht vor, dass die Beteiligung der Bundeswehr an der internationalen Kosovo Force (KFOR) im Kosovo verlängert wird. Bei dem Einsatz handelt es sich um die Unterstützung deutscher Streitkräfte an der Entwicklung eines "stabilen, demokratischen, multiethnischen und friedlichen Kosovos".</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD stimmten der Verlängerung ebenso zu wie die Fraktionen von FDP und Grünen. Damit wurde der Antrag angenommen. AfD und Linke votierten jeweils geschlossen gegen den Antrag.</p>\r\n',
                        "field_poll_date": "2020-06-17",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 362747,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Verlängerung des Bundeswehreinsatzes in Mali (MINUSMA 2020/2021)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/362747",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3668,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3668,
                        "label": "Verlängerung des Bundeswehreinsatzes in Mali (MINUSMA 2020/2021)",
                        "field_intro": '<p>Der von der Bundesregierung eingebrachte <a href="https://dip21.bundestag.de/dip21/btd/19/190/1919002.pdf">Antrag </a>sieht vor, dass das Bundeswehrmandat für die Beteiligung an der UN-Mission MINUSMA verlängert wird. Bei dem Einsatz handelt es sich um die Beteiligung bewaffneter deutscher Streitkräfte an der "Multidimensionalen Integrierten Stabilisierungsmission der Vereinten Nationen in Mali (MINUSMA)".</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD stimmten der Verlängerung ebenso zu wie die Grüne- und FDP-Fraktion. Damit wurde der Antrag angenommen. Die AfD- und Linksfraktion votierte geschlossen gegen den Antrag. Bei den Grünen kam es zu fünf Enthaltungen und drei Nein-Stimmen.</p>\r\n',
                        "field_poll_date": "2020-05-29",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 362038,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Verlängerung des Bundeswehreinsatzes in Mali (EUTM Mali 2020/2021)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/362038",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3669,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3669,
                        "label": "Verlängerung des Bundeswehreinsatzes in Mali (EUTM Mali 2020/2021)",
                        "field_intro": '<p>Der von der Bundesregierung eingebrachte <a href="https://dip21.bundestag.de/dip21/btd/19/190/1919002.pdf">Antrag </a>sieht vor, dass die Beteiligung der Bundeswehr an der Militärmission <a href="https://eutmmali.eu/">EUTM</a> verlängert wird. Bei dem Einsatz handelt es sich um die Beteiligung deutscher Streitkräfte an dem Beitrag der Europäischen Union zur Ausbildung der malischen Streitkräfte.</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD stimmten der Verlängerung ebenso zu wie die FDP-Fraktion. Damit wurde der Antrag angenommen. Die AfD- und Linksfraktion votierte geschlossen gegen den Antrag. Die Grünen enthielten sich zum großen Teil ihrer Stimme.</p>\r\n',
                        "field_poll_date": "2020-05-29",
                        "poll_passed": True,
                    },
                },
            ],
            "topic_ids_of_latest_committee": [],
        },
        {
            "id": 78974,
            "label": "Max Straubinger",
            "party": {
                "id": 3,
                "label": "CSU",
                "party_style": {
                    "id": 3,
                    "display_name": "CSU",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#0D6CB4",
                    "border_color": "#F8F8F8",
                },
            },
            "occupations": ["MdB"],
            "sidejobs": [
                {
                    "id": 11680,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2021-09-06",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 11679,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2021-09-06",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9973,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-08-24",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9965,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-08-14",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9768,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Verwaltungsrates, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2020-06-22",
                    "sidejob_organization": {
                        "id": 3796,
                        "entity_type": "sidejob_organization",
                        "label": "DONAUISAR Klinikum Deggendorf-Dingolfing-Landau gKU",
                    },
                },
                {
                    "id": 9176,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "3.500 € bis 7.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9175,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9174,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9173,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9172,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 9171,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 8408,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter (bis 30.09.2019)",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2019-05-21",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 7223,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2018-05-31",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 5841,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 5838,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 5837,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 2951,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Parlamentarischen Beirates",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 370,
                        "entity_type": "sidejob_organization",
                        "label": "Versicherungsombudsmann e.V.",
                    },
                },
                {
                    "id": 2949,
                    "entity_type": "sidejob",
                    "label": "Präsident",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2196,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsches Institut für Reines Bier e.V.",
                    },
                },
                {
                    "id": 2947,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 2946,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Kreistages, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 373,
                        "entity_type": "sidejob_organization",
                        "label": "Landkreis Dingolfing-Landau",
                    },
                },
                {
                    "id": 2944,
                    "entity_type": "sidejob",
                    "label": "Vertreter (bis 30.09.2019)",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 372,
                        "entity_type": "sidejob_organization",
                        "label": "Münchener und Magdeburger Agrarversicherung AG",
                    },
                },
                {
                    "id": 2942,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2941,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "150.000 € bis 250.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2940,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "150.000 € bis 250.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2939,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2938,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "15.000 € bis 30.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2930,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 2926,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 2925,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
            ],
            "cvs": [
                {
                    "id": 571,
                    "short_description": "Geboren am 12. August 1954 in Oberlucken; römisch-katholisch; verheiratet; drei Kinder.",
                    "politician_id": 78974,
                    "raw_text": "1973 bis 1974 Grundwehrdienst in München;1970 Gründungsmitglied JU-Ortsverband Simbach; 1985 bis 1989 JU-Kreisvorsitzender Im JU-Kreisverband Dingolfing-Landau;1972 Eintritt in die CSU; 1987 bis 1993 stellvertretender CSU-Kreisvorsitzender; seit 1993 CSU-Kreisvorsitzender im Kreisverband Dingolfing-Landau; 1978 bis 1994 Mitglied des Marktrates von Simbach; seit 1990 Mitglied im Kreistag Dingolfing-Landau MdB; seit 1994 Wahlkreis Rottal-Inn; 2002 bis Dezember 2013 stellvertretender Vorsitzender der CSU-Landesgruppe im Deutschen Bundestag; 2005  bis Dezember 2013 Arbeits- sozial- und gesundheitspolitischer Sprecher der CSU-Landesgruppe im Deutschen Bundestag;  2009  bis Dezember 2013 stellvertretender Vorsitzender des Ausschusses für Arbeit und Soziales im Deutschen Bundestag; 2013 bis 2017 Parlamentarischer Geschäftsführer der CSU-Landesgruppe im Deutschen Bundestag. ",
                }
            ],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/max-straubinger",
            "weblinks": [
                {
                    "link": "http://www.max-straubinger.de/",
                    "id": 44551,
                    "politician_id": 78974,
                },
                {
                    "link": "https://de.wikipedia.org/wiki/Max_Straubinger",
                    "id": 44552,
                    "politician_id": 78974,
                },
                {
                    "link": "https://www.facebook.com/MaxStraubingerMdB",
                    "id": 44553,
                    "politician_id": 78974,
                },
            ],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 482126,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Weiterbetrieb deutscher Atomkraftwerke bis zum 15. April 2023",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/482126",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4828,
                        "vote": "no",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4828,
                        "label": "Weiterbetrieb deutscher Atomkraftwerke bis zum 15. April 2023",
                        "field_intro": '<p>Der <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/042/2004217.pdf">Gesetzentwurf </a>der Bundesregierung fordert eine Laufzeitverlängerung für die noch in Betrieb befindlichen drei deutschen Atomkraftwerke bis zum 15. April 2023. Hintergrund des Entwurfs ist die aktuelle Diskussion um die Energieversorgungssituation in Deutschland im Winter 2022/2023.</p>\r\n\r\n<p>Der Gesetzentwurf wurde vom Bundestag <strong>angenommen</strong>. 375 Abgeordnete der Ampel-Koalition stimmten für den Antrag. Es gab 216 Gegenstimmen, größtenteils aus der Unionsfraktion und der Linkspartei. Außerdem stimmten neun Grüne-Abgeordnete gegen den Gesetzentwurf. Insgesamt 70 Enthaltungen kamen mehrheitlich aus der AfD-Fraktion.</p>\r\n',
                        "field_poll_date": "2022-11-11",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 480654,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Wahlwiederholung der Bundestagswahl in 431 Berliner Wahlbezirken",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/480654",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4827,
                        "vote": "no",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4827,
                        "label": "Wahlwiederholung der Bundestagswahl in 431 Berliner Wahlbezirken",
                        "field_intro": '<p>Die <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/040/2004000.pdf">Beschlussempfehlung </a>des <a class="link-committees" href="https://www.abgeordnetenwatch.de/bundestag/20/ausschuesse/ausschuss-fuer-wahlpruefung-immunitaet-und-geschaeftsordnung">Wahlprüfungsausschusses </a>schlägt eine Wiederholung der Bundestagswahl in 431 Berliner Wahllokalen bezüglich der Erst- und der Zweitstimme vor. Wahllokale in allen Berliner Wahlkreisen sind von der Wahlwiederholung betroffen.</p>\r\n\r\n<p>Der Bundestag stimmte der Beschlussempfehlung zu. Die <strong>Bundestagswahl wird in 431 Berliner Wahllokalen wiederholt</strong>. Für die Anahme der Einsprüche stimmten insgesamt 374 Abgeordnete aus SPD, Bündnis 90/Die Grünen und FDP. Abgeordnete der Unionsfraktion sowie der AfD stimmten mit ingesamt 252 Stimmen gegen eine Wahlwiederholung. 31 Enthaltungen kamen mehrheitlich aus der Fraktion der Linkspartei.</p>\r\n',
                        "field_poll_date": "2022-11-11",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 481390,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Änderung des Infektionsschutzgesetzes (Triage-Entscheidungen)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/481390",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4832,
                        "vote": "no",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4832,
                        "label": "Änderung des Infektionsschutzgesetzes (Triage-Entscheidungen)",
                        "field_intro": '<p>Der <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/038/2003877.pdf">Gesetzentwurf</a> der Bundesregierung zur Änderung des Infektionsschutzgesetzes legt Regeln zu zukünftigen Triage-Entscheidungen auf Intensivstationen fest. Abgestimmt wurde über eine Beschlussempfehlung des Gesundheitsausschusses, die empfahl den Entwurf anzunehmen.</p>\r\n\r\n<p>Die Beschlussempfehlung wurde mit 366 Stimmen aus der Koalitionsfraktionen <strong>angenommen</strong>. Es gab 284 Gegenstimmen aus den Fraktionen der CDU/CSU, der AfD und der Fraktion Die Linke. Fünf Abgeordnete enthielten sich.</p>\r\n',
                        "field_poll_date": "2022-11-10",
                        "poll_passed": False,
                    },
                },
                {
                    "Vote": {
                        "id": 479918,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Vermögensabgabe für Milliardär:innen und Multimillionär:innen (Antrag)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/479918",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4830,
                        "vote": "no",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4830,
                        "label": "Vermögensabgabe für Milliardär:innen und Multimillionär:innen (Antrag)",
                        "field_intro": '<p>Mit dem <a href="https://dserver.bundestag.de/btd/20/043/2004307.pdf">Antrag</a> der Fraktion Die Linke wurde über eine einmalige Vermögensabgabe für Milliardär:innen und Multimillionär:innen abgestimmt. Die so gewonnen Einnahmen sollen zur Abfederung der finanziellen Belastung der Bevölkerung durch die Energiepreiskrise genutzt werden.</p>\r\n\r\n<p>Der Antrag wurde mit 649 Stimmen aus den Fraktionen von SPD, Bündnis 90/Die Grünen, FDP, CDU/CSU und der AfD <strong>abgelehnt</strong>. Lediglich die anwesenden Abgeordneten der Linken stimmten mit 36 Ja-Stimmen für den Antrag. Es gab keine Enthaltungen.</p>\r\n',
                        "field_poll_date": "2022-11-10",
                        "poll_passed": False,
                    },
                },
                {
                    "Vote": {
                        "id": 479182,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Inflationsausgleichsgesetz",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/479182",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4831,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4831,
                        "label": "Inflationsausgleichsgesetz",
                        "field_intro": '<p>Der Bundestag stimmte über einen <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/034/2003496.pdf">Gesetzentwurf </a>der Koaltitionsfraktionen ab. Mit dem Inflationsausgleichsgesetz sollen die Effekte der Inflation ausgeglichen werden. Dies soll mit einem angepassten Einkommenssteuertarif und weiteren steuerliche Regelungen errreicht werden.</p>\r\n\r\n<p>Der Gesetzentwurf wurde mit 578 Stimmen von Seiten der Regierungsfraktionen und der Fraktion der CDU/CSU <strong>angenommen</strong>. 35 Abgeordnete der Fraktion Die Linke stimmten gegen den Entwurf. 75 Abgeordnete enthielten sich, darunter die AfD-Fraktion.</p>\r\n',
                        "field_poll_date": "2022-11-10",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 478446,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Einführung des Bürgergeldes",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/478446",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4826,
                        "vote": "no",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4826,
                        "label": "Einführung des Bürgergeldes",
                        "field_intro": '<p>Der <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/038/2003873.pdf">Gesetzentwurf </a>der Bundesregierung fordert die Einführung des sogenannten Bürgergeldes. Der Hartz IV-Nachfolger soll die Grundsicherung für arbeitssuchende Menschen sicherstellen.</p>\r\n\r\n<p>Der Gesetzentwurf wurde mit 385 Stimmen von Seiten der Ampel-Koalition aus SPD, Bündnis 90/Die Grünen und FDP <strong>angenommen</strong>. Die Fraktionen CDU/CSU sowie die AfD stimmten dabei gegen den Gesetzentwurf. Die Abgeordneten der Fraktion Die Linke enthielten sich.</p>\r\n',
                        "field_poll_date": "2022-11-10",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 475593,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Verlängerung des Bundeswehreinsatzes im Irak (2023)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/475593",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4804,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4804,
                        "label": "Verlängerung des Bundeswehreinsatzes im Irak (2023)",
                        "field_intro": '<p>Mit dem <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/038/2003818.pdf">Antrag </a>der Bundesregierung soll über die Fortsetzung des Bundeswehreinsatzes im Irak bis zum 31. Oktober 2023 entschieden werden. Mit der Verlängerung des bereits laufenden Bundeswehreinsatzes soll das erneute Erstarken des sogenannten Islamischen Staates verhindert und die Versöhnung der Konfliktparteien Irak und Syrien gefördert werden<strong>. </strong></p>\r\n\r\n<p>Der Antrag wurde mit 534 Stimmen von den Fraktionen SPD, CDU/CSU, Bündnis 90/Die Grüne und FDP angenommen. Dagegen gestimmt haben die Fraktionen AfD und Die Linke.</p>\r\n',
                        "field_poll_date": "2022-10-21",
                        "poll_passed": True,
                    },
                },
                {
                    "Vote": {
                        "id": 474121,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Abwehrschirm gegen gestiegene Strom- und Gaspreise",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/474121",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4803,
                        "vote": "no",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4803,
                        "label": "Abwehrschirm gegen gestiegene Strom- und Gaspreise",
                        "field_intro": '<p>Mit dem <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/040/2004058.pdf">Antrag </a>der Regierungsfraktionen in Form einer Gesetzesänderung soll die rechtliche Grundlage zur Umsetzung eines finanziellen "Abwehrschirms" geschaffen werden, um den Folgen der gestiegenen Gas- und Strompreise entgegenzuwirken. Der Antrag soll die vorgesehene Kreditaufnahme ermöglichen.</p>\r\n\r\n<p>Der Antrag wurde mit den Stimmen der Regierungsfraktionen<strong> </strong>SPD, Bündnis 90/Die Grünen und FDP<strong> angenommen</strong>. Von der CDU/CSU-Fraktion stimmte allein <a href="https://www.abgeordnetenwatch.de/profile/jonas-geissler">Dr. Jonas Geissler</a> für den Antrag, alle anderen Unionsabgeordneten stimmten dagegen. Auch die AfD wandte sich geschlossen gegen den Antrag, während sich die Fraktion DIE LINKE enthielt.<br />\r\nInsgesamt stimmten 390 Abgeordnete für den Beschluss, 239 dagegen und 36 enthielten sich.</p>\r\n',
                        "field_poll_date": "2022-10-21",
                        "poll_passed": True,
                    },
                },
            ],
            "topic_ids_of_latest_committee": [2, 5, 14, 28],
        },
    ]

    response = client.get(
        "/v1/politicians/?ids=78973&ids=78974?votes_start=8&votes_end=9"
    )
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
            "occupations": ["MdB"],
            "sidejobs": [
                {
                    "id": 6893,
                    "entity_type": "sidejob",
                    "label": "Vorsitzende",
                    "income_level": None,
                    "interval": None,
                    "created": "2018-04-16",
                    "sidejob_organization": {
                        "id": 914,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsch-Kasachische Gesellschaft e.V.",
                    },
                },
                {
                    "id": 4541,
                    "entity_type": "sidejob",
                    "label": "Stellv. Vorsitzende, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-09-23",
                    "sidejob_organization": {
                        "id": 914,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsch-Kasachische Gesellschaft e.V.",
                    },
                },
                {
                    "id": 413,
                    "entity_type": "sidejob",
                    "label": "Beteiligung (bis 31.12.2014)",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 872,
                        "entity_type": "sidejob_organization",
                        "label": "Karin Strenz GbR",
                    },
                },
                {
                    "id": 412,
                    "entity_type": "sidejob",
                    "label": "Beratung - Line M-Trade GmbH, Nürnberg (bis Ende Januar 2015)",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 3183,
                        "entity_type": "sidejob_organization",
                        "label": "Beratung - selbständig",
                    },
                },
                {
                    "id": 411,
                    "entity_type": "sidejob",
                    "label": "Beratung - Line M-Trade GmbH, Nürnberg (bis Ende Januar 2015)",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-23",
                    "sidejob_organization": {
                        "id": 3183,
                        "entity_type": "sidejob_organization",
                        "label": "Beratung - selbständig",
                    },
                },
            ],
            "cvs": [
                {
                    "id": 633,
                    "short_description": "Geboren am 14. Oktober 1967 in Lübz; evangelisch-lutherisch; verheiratet.",
                    "politician_id": 78973,
                    "raw_text": "Besuch der Polytechnischen Oberschule Lübz; Studium am Institut für Lehrerbildung in Rostock; Studium an der Pädagogischen Hochschule in Magdeburg; Abschluss als Diplom-Lehrerin für Sonderschulen; Zusatzstudium der Erziehungswissenschaften an der Goethe-Universität Frankfurt/Main. Lehrerin an der Sonderschule in Wanzleben bei Magdeburg; 1992 bis 2002 Angestellte einer Import- und Großhandelsfirma in Frankfurt/Main. Seit 2015 Vorsitzende der Deutsch-Kasachischen-Gesellschaft e. V. Seit 2001 Vorsitzende des CDU-Kreisverbandes Parchim; 1999 bis 2005 Mitglied des CDU-Landesvorstandes; 2001 bis 2005 Stellvertretende CDU-Landesvorsitzende; Mitglied der Christlich-Demokratische Arbeitnehmerschaft (CDA); seit 2013 Ehrenvorsitzende CDU-Kreisverband Ludwigslust-Parchim. Seit 1999 Mitglied des Kreistages zu Parchim; seit 2001 Vorsitzende der CDU-Kreistagsfraktion Parchim; seit 2002 Mitglied des Landtages von Mecklenburg-Vorpommern; Ausschüsse: Wirtschaft, Arbeit, Bau und Landesentwicklung, Petitionsausschuss; 2002 bis 2006 arbeitsmarktpolitische Sprecherin der CDU-Fraktion; seit November 2007 verantwortlich für das Sorgentelefon der CDU-Fraktion; 2006 bis 2008 Aufsichtsratsvorsitzende des Flughafens Parchim. Mitglied des Deutschen Bundestages seit Oktober 2009. Karin Strenz ist am 21. März 2021 verstorben, Nachfolgerin ist die Abgeordnete Maika Friemann-Jennert, CDU/CSU. ** verstorben ",
                }
            ],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/karin-strenz",
            "weblinks": [
                {
                    "politician_id": 78973,
                    "id": 44558,
                    "link": "https://www.wahl.de/politiker/cdu/karin-strenz",
                },
                {"politician_id": 78973, "id": 44559, "link": "http://www.strenz.de/"},
                {
                    "politician_id": 78973,
                    "id": 44560,
                    "link": "https://www.wen-waehlen.de/btw09/kandidaten/karin-strenz_10058.html",
                },
                {
                    "politician_id": 78973,
                    "id": 44561,
                    "link": "https://de.wikipedia.org/wiki/Karin_Strenz",
                },
                {
                    "politician_id": 78973,
                    "id": 44562,
                    "link": "https://www.facebook.com/Karin.Strenz",
                },
            ],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 361329,
                        "entity_type": "vote",
                        "label": "Karin Strenz - Verlängerung des Bundeswehreinsatzes in Somalia (Atalanta 2020/2021)",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/361329",
                        "mandate_id": 45423,
                        "fraction_id": 81,
                        "poll_id": 3667,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 3667,
                        "label": "Verlängerung des Bundeswehreinsatzes in Somalia (Atalanta 2020/2021)",
                        "field_intro": '<p>Der von der Bundesregierung eingebrachte <a href="https://dip21.bundestag.de/dip21/btd/19/188/1918866.pdf">Antrag </a>sieht vor, dass die Operation <a href="https://eunavfor.eu/">ATALANTA</a>, an der sich die Bundeswehr beteiligt, verlängert wird. Bei dem Einsatz handelt es sich um die Beteiligung deutscher Streitkräfte an einer maritimen Operation der EU, vor der Küste Somalias, mit der Aufgabe, die Piraterie zu bekämpfen und die Gebiete zu überwachen. Abgestimmt wurde über die <a href="https://dip21.bundestag.de/dip21/btd/19/191/1919196.pdf">Beschlussempfehlung </a>des federführenden<a href="https://www.abgeordnetenwatch.de/bundestag/19/ausschuesse/auswaertiger-ausschuss"> Auswärtigen Ausschusses</a>.</p>\r\n\r\n<p>Die Regierungsfraktionen CDU/CSU und SPD stimmten dem Antrag ebenso zu wie die Fraktionen AfD und FDP. Damit wurde der Antrag angenommen. Die Linksfraktion votierte geschlossen gegen den Antrag. Bei den Grünen gab es Zustimmungen und einige Nein-Stimmen, die Hälfte der Fraktion enthielt sich.</p>\r\n',
                        "field_poll_date": "2020-05-27",
                        "poll_passed": True,
                    },
                }
            ],
            "topic_ids_of_latest_committee": [],
        },
        {
            "id": 78974,
            "label": "Max Straubinger",
            "party": {
                "id": 3,
                "label": "CSU",
                "party_style": {
                    "id": 3,
                    "display_name": "CSU",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#0D6CB4",
                    "border_color": "#F8F8F8",
                },
            },
            "occupations": ["MdB"],
            "sidejobs": [
                {
                    "id": 11680,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2021-09-06",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 11679,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2021-09-06",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9973,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-08-24",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9965,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-08-14",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9768,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Verwaltungsrates, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2020-06-22",
                    "sidejob_organization": {
                        "id": 3796,
                        "entity_type": "sidejob_organization",
                        "label": "DONAUISAR Klinikum Deggendorf-Dingolfing-Landau gKU",
                    },
                },
                {
                    "id": 9176,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "3.500 € bis 7.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9175,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9174,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 9173,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 9172,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 9171,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2020-01-02",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 8408,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter (bis 30.09.2019)",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2019-05-21",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 7223,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2018-05-31",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 5841,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": "1.000 € bis 3.500 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 5838,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 5837,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2018-02-05",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 2951,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Parlamentarischen Beirates",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 370,
                        "entity_type": "sidejob_organization",
                        "label": "Versicherungsombudsmann e.V.",
                    },
                },
                {
                    "id": 2949,
                    "entity_type": "sidejob",
                    "label": "Präsident",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2196,
                        "entity_type": "sidejob_organization",
                        "label": "Deutsches Institut für Reines Bier e.V.",
                    },
                },
                {
                    "id": 2947,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Beirates für sparkassenpolitische Grundsatzfragen",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 371,
                        "entity_type": "sidejob_organization",
                        "label": "Sparkassenverband Bayern",
                    },
                },
                {
                    "id": 2946,
                    "entity_type": "sidejob",
                    "label": "Mitglied des Kreistages, ehrenamtlich",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 373,
                        "entity_type": "sidejob_organization",
                        "label": "Landkreis Dingolfing-Landau",
                    },
                },
                {
                    "id": 2944,
                    "entity_type": "sidejob",
                    "label": "Vertreter (bis 30.09.2019)",
                    "income_level": None,
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 372,
                        "entity_type": "sidejob_organization",
                        "label": "Münchener und Magdeburger Agrarversicherung AG",
                    },
                },
                {
                    "id": 2942,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2941,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "150.000 € bis 250.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2940,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "150.000 € bis 250.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2939,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "100.000 € bis 150.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2938,
                    "entity_type": "sidejob",
                    "label": "Generalvertreter",
                    "income_level": "15.000 € bis 30.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 2194,
                        "entity_type": "sidejob_organization",
                        "label": "Allianz Beratungs- und Vertriebs AG",
                    },
                },
                {
                    "id": 2930,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 1130,
                        "entity_type": "sidejob_organization",
                        "label": "Baywa AG",
                    },
                },
                {
                    "id": 2926,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
                {
                    "id": 2925,
                    "entity_type": "sidejob",
                    "label": "Landwirt - selbständig",
                    "income_level": "7.000 € bis 15.000 €",
                    "interval": None,
                    "created": "2017-05-29",
                    "sidejob_organization": {
                        "id": 3720,
                        "entity_type": "sidejob_organization",
                        "label": "Hingerl GmbH",
                    },
                },
            ],
            "cvs": [
                {
                    "id": 571,
                    "short_description": "Geboren am 12. August 1954 in Oberlucken; römisch-katholisch; verheiratet; drei Kinder.",
                    "politician_id": 78974,
                    "raw_text": "1973 bis 1974 Grundwehrdienst in München;1970 Gründungsmitglied JU-Ortsverband Simbach; 1985 bis 1989 JU-Kreisvorsitzender Im JU-Kreisverband Dingolfing-Landau;1972 Eintritt in die CSU; 1987 bis 1993 stellvertretender CSU-Kreisvorsitzender; seit 1993 CSU-Kreisvorsitzender im Kreisverband Dingolfing-Landau; 1978 bis 1994 Mitglied des Marktrates von Simbach; seit 1990 Mitglied im Kreistag Dingolfing-Landau MdB; seit 1994 Wahlkreis Rottal-Inn; 2002 bis Dezember 2013 stellvertretender Vorsitzender der CSU-Landesgruppe im Deutschen Bundestag; 2005  bis Dezember 2013 Arbeits- sozial- und gesundheitspolitischer Sprecher der CSU-Landesgruppe im Deutschen Bundestag;  2009  bis Dezember 2013 stellvertretender Vorsitzender des Ausschusses für Arbeit und Soziales im Deutschen Bundestag; 2013 bis 2017 Parlamentarischer Geschäftsführer der CSU-Landesgruppe im Deutschen Bundestag. ",
                }
            ],
            "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/max-straubinger",
            "weblinks": [
                {
                    "politician_id": 78974,
                    "id": 44551,
                    "link": "http://www.max-straubinger.de/",
                },
                {
                    "politician_id": 78974,
                    "id": 44552,
                    "link": "https://de.wikipedia.org/wiki/Max_Straubinger",
                },
                {
                    "politician_id": 78974,
                    "id": 44553,
                    "link": "https://www.facebook.com/MaxStraubingerMdB",
                },
            ],
            "votes_and_polls": [
                {
                    "Vote": {
                        "id": 473385,
                        "entity_type": "vote",
                        "label": "Max Straubinger - Änderung des Bundeszentralregistergesetzes",
                        "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/473385",
                        "mandate_id": 53923,
                        "fraction_id": 320,
                        "poll_id": 4808,
                        "vote": "yes",
                        "reason_no_show": None,
                        "reason_no_show_other": None,
                    },
                    "Poll": {
                        "id": 4808,
                        "label": "Änderung des Bundeszentralregistergesetzes",
                        "field_intro": '<p>Der <a class="link-read-more" href="https://dserver.bundestag.de/btd/20/037/2003708.pdf">Gesetzentwurf </a>der Bundesregierung schlägt Änderungen am Bundeszentralregistergesetz (BZRG) vor. Mit den vorgeschlagenen Änderungen soll das BZRG an die Bestimmungen des Handels- und Kooperationsabkommens zwischen der Europäischen Union und Großbritannien angepasst werden.</p>\r\n\r\n<p>Durch den Rechtsausschuss wurde der Entwurf ergänzt, sodass zukünfitg die Strafbarkeit der öffentlichen Billigung, Leugnung und gröblichen Verharmlosung von Völkermord, Verbrechen gegen die Menschlichkeit und Kriegsverbrechen explizit in das Strafgesetzbuch aufgenommen werden. Der Paragraf 130 StGB, welcher den Tatbestand der Volksverhetzung definiert, soll um einen neuen Absatz ergänzt werden.</p>\r\n\r\n<p>Für den Entwurf stimmten die&nbsp; 514 Abgeordneten der Regierungskoalition sowie der Unionsfraktion geschlossen. Gegen den Entwurf stimmten die AfD sowie bis auf <a href="https://www.abgeordnetenwatch.de/profile/petra-sitte">Dr. Petra Sitte</a> auch die Linksfraktion. Neben Petra Sitte enthielt sich auch der fraktionslose Abgeordnete <a href="https://www.abgeordnetenwatch.de/profile/stefan-seidler">Stefan Seidler</a>.</p>\r\n',
                        "field_poll_date": "2022-10-20",
                        "poll_passed": True,
                    },
                }
            ],
            "topic_ids_of_latest_committee": [2, 5, 14, 28],
        },
    ]


# Move to v2 tests
# def test_politicians_route_multiple_ids_invalid_parameters():
#     response = client.get(
#         "/v1/politicians/?ids=78973&ids=78974?votes_start=-10&votes_end=-2"
#     )
#     # assert user friendly error message, don't allow negative integers (confirm design)
#     response = client.get(
#         "/v1/politicians/?ids=78973&ids=78974?votes_start=.03&votes_end=1.6"
#     )
#     # assert user friendly error message, don't allow floats
#     response = client.get(
#         "/v1/politicians/?ids=78973&ids=78974?votes_start=sandwich&votes_end=banana"
#     )
#     # assert user friendly error message, don't allow strings


def test_politicians_route_does_not_exist_single_id():
    response = client.get("/v1/politicians/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_politicians_route_does_not_exist_multiple_nonexisting_ids():
    response = client.get("/v1/politicians/?ids=1&ids=2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politician not found"}


def test_politicians_route_does_not_exist_duplicate_ids():
    response = client.get("/v1/politicians/?ids=1&ids=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politician not found"}


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
    response = client.get("v1/search?text=0")
    assert response.status_code == 404
    assert response.json() == {"detail": "Politicians not found"}


def test_polls_expected_results():
    response = client.get("v1/polls/28881?filters=1")
    assert response.status_code == 200
    assert type(response.json()) is list


def test_polls_filter():
    response = client.get("v1/polls/28881")
    assert response.status_code == 200
    assert type(response.json()) is list


def test_polls_does_not_exist():
    response = client.get("v1/polls/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Polls not found"}


def test_poll_votes_expected_results():
    response = client.get("v1/poll/4830/votes")
    assert response.status_code == 200
    assert type(response.json()) is dict


def test_poll_votes_does_not_exist():
    response = client.get("v1/poll/0/votes")
    assert response.status_code == 404
    assert response.json() == {"detail": "Votes not found"}


def test_bundestag_speeches_expected_results():
    response = client.get("v1/bundestag/speeches?page=1")
    assert response.status_code == 200
    assert type(response.json()) is dict


# def test_bundestag_speeches_invalid_parameter():
#     response = client.get("v1/bundestag/speeches?page=-1")
#     assert response.status_code == 500


def test_bundestag_polls_expected_results():
    response = client.get("v1/bundestag/polls?follow_ids=1")
    assert type(response.json()) is list


def test_bundestag_polls_expected_results():
    response = client.get("v1/bundestag/allpolls")
    assert type(response.json()) is dict


def test_party_donations():
    response = client.get("v1/partydonations")
    assert type(response.json()) is list
