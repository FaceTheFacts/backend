# std
from typing import List
from src.cron_jobs.utils.file import read_json

# local
from src.cron_jobs.utils.insert_and_update import insert_and_update
from src.cron_jobs.utils.fetch import (
    fetch_missing_entity,
    load_entity,
)
from src.db.connection import engine, Base
import src.db.models as models


def append_committees() -> List:
    missing_committees = fetch_missing_entity("committees", models.Committee)
    if missing_committees:
        committees = [
            {
                "id": api_committees["id"],
                "entity_type": api_committees["entity_type"],
                "label": api_committees["label"],
                "api_url": api_committees["api_url"],
                "field_legislature_id": api_committees["field_legislature"]["id"]
                if api_committees["field_legislature"]
                else None,
            }
            for api_committees in missing_committees
        ]
        insert_and_update(models.Committee, committees)
        print("Successfully retrieved")
        return committees
    else:
        print("Nothing fetched")


def append_sidejobs() -> List:
    missing_sidejobs = fetch_missing_entity("sidejobs", models.Sidejob)
    if missing_sidejobs:
        sidejobs = [
            {
                "id": api_sidejob["id"],
                "entity_type": api_sidejob["entity_type"],
                "label": api_sidejob["label"],
                "api_url": api_sidejob["api_url"],
                "job_title_extra": api_sidejob["job_title_extra"],
                "additional_information": api_sidejob["additional_information"],
                "category": api_sidejob["category"],
                "income_level": api_sidejob["income_level"],
                "interval": api_sidejob["interval"],
                "data_change_date": api_sidejob["data_change_date"],
                "created": api_sidejob["created"],
                "sidejob_organization_id": api_sidejob["sidejob_organization"]["id"]
                if api_sidejob["sidejob_organization"]
                else None,
                "field_city_id": api_sidejob["field_city"]["id"]
                if api_sidejob["field_city"]
                else None,
                "field_country_id": api_sidejob["field_country"]["id"]
                if api_sidejob["field_country"]
                else None,
            }
            for api_sidejob in missing_sidejobs
        ]
        insert_and_update(models.Sidejob, sidejobs)
        print("Successfully retrieved")
        return sidejobs
    else:
        print("Nothing fetched")


def append_polls() -> List:
    missing_polls = fetch_missing_entity("polls", models.Poll)
    if missing_polls:
        polls = [
            {
                "id": api_polls["id"],
                "entity_type": api_polls["entity_type"],
                "label": api_polls["label"],
                "api_url": api_polls["api_url"],
                "field_committees_id": api_polls["field_committees"][0]["id"]
                if api_polls["field_committees"]
                else None,
                "field_intro": api_polls["field_intro"],
                "field_legislature_id": api_polls["field_legislature"]["id"]
                if api_polls["field_legislature"]
                else None,
                "field_poll_date": api_polls["field_poll_date"],
            }
            for api_polls in missing_polls
        ]
        insert_and_update(models.Poll, polls)
        print("Successfully retrieved")
        return polls
    else:
        print("Nothing fetched")


def append_votes() -> List:
    missing_votes = fetch_missing_entity("votes", models.Vote)
    if missing_votes:
        api_polls = load_entity("polls")
        poll_ids = set([api_poll["id"] for api_poll in api_polls])
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


def append_parties() -> List:
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


def append_politicians() -> List:
    # Before appending politicians we need to check if there new parties as party_id is a foreign key in politicians
    append_parties()

    # Now we can append politicians
    # First we need to fetch the missing politicians
    # Use command below when having already fetch the politicians
    # missing_politicians = read_json("src/cron_jobs/data/politicians.json")
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
                "deceased": api_politician["deceased"],
                "deceased_date": api_politician["deceased_date"],
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


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # append_politicians()
