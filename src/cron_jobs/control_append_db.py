from src.cron_jobs.utils.control_utils import (
    fetch_missing_entity,
    load_entity_ids_from_db,
    insert_and_update,
)
from src.db import models


def append_votes():
    missing_votes = fetch_missing_entity("votes", models.Vote)
    if missing_votes:
        poll_ids = load_entity_ids_from_db(models.Poll)
        votes = []
        for missing_vote in missing_votes:
            poll_id = missing_vote["poll"]["id"] if missing_vote["poll"] else None
            if poll_id in poll_ids:
                vote = {
                    "id": missing_vote["id"],
                    "entity_type": missing_vote["entity_type"],
                    "label": missing_vote["label"],
                    "api_url": missing_vote["api_url"],
                    "mandate_id": missing_vote["mandate"]["id"]
                    if missing_vote["mandate"]
                    else None,
                    "fraction_id": missing_vote["fraction"]["id"]
                    if missing_vote["fraction"]
                    else None,
                    "poll_id": poll_id,
                    "vote": missing_vote["vote"],
                    "reason_no_show": missing_vote["reason_no_show"],
                    "reason_no_show_other": missing_vote["reason_no_show_other"],
                }
                votes.append(vote)
        insert_and_update(models.Vote, votes)
        print("Successfully retrieved")
        return votes
    else:
        print("Nothing fetched")


def append_parties():
    missing_parties = fetch_missing_entity("parties", models.Party)
    if missing_parties:
        parties = [
            {
                "id": api_party["id"],
                "entity_type": api_party["entity_type"],
                "label": api_party["label"],
                "api_url": api_party["api_url"],
                "full_name": api_party["full_name"],
                "short_name": api_party["short_name"],
                "party_style_id": api_party["id"],
            }
            for api_party in missing_parties
        ]
        party_styles = [
            {
                "id": api_party["id"],
                "display_name": api_party["label"],
                "foreground_color": "#FFFFFF",
                "background_color": "#333333",
                "border_color": None,
            }
            for api_party in parties
        ]
        insert_and_update(models.PartyStyle, party_styles)
        insert_and_update(models.Party, parties)
        print("Successfully updated party styles and parties")
    print("Nothing to fetch for parties and party styles")


def append_politicians():
    missing_politicians = fetch_missing_entity("politicians", models.Politician)
    if missing_politicians:
        politicians = [
            {
                "id": api_politician["id"],
                "entity_type": api_politician["entity_type"],
                "label": api_politician["label"],
                "api_url": api_politician["api_url"],
                "abgeordnetenwatch_url": api_politician["abgeordnetenwatch_url"],
                "first_name": api_politician["first_name"],
                "last_name": api_politician["last_name"],
                "birth_name": api_politician["birth_name"],
                "sex": api_politician["sex"],
                "year_of_birth": api_politician["year_of_birth"],
                "party_id": api_politician["party"]["id"]
                if api_politician["party"]
                else None,
                "party_past": api_politician["party_past"],
                "deceased": None,
                "deceased_date": None,
                "education": api_politician["education"],
                "residence": api_politician["residence"],
                "occupation": api_politician["occupation"],
                "statistic_questions": api_politician["statistic_questions"],
                "statistic_questions_answered": api_politician[
                    "statistic_questions_answered"
                ],
                "qid_wikidata": api_politician["qid_wikidata"],
                "field_title": api_politician["field_title"],
            }
            for api_politician in missing_politicians
        ]
        insert_and_update(models.Politician, politicians)
        print("Successfully retrieved politicians")
        return politicians
    else:
        print("Nothing to fetch for politicians")
