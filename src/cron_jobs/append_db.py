# local
from src.cron_jobs.utils.insert_and_update import insert_and_update
from src.cron_jobs.utils.fetch import fetch_missing_entity, load_entity
from src.db.connection import engine, Base
import src.db.models as models


def append_sidejobs() -> None:
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
        return sidejobs
    else:
        print("Nothing fetched")


def append_polls() -> None:
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


def append_votes() -> None:
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


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    append_sidejobs()
    # append_polls()
    # append_votes()
