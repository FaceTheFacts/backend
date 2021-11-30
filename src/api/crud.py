import json
import urllib.request
from typing import List

# third-party
from sqlalchemy.orm import Session

from sqlalchemy import text, or_

# local
import src.db.models as models
from src.api.utils.read_url import load_json_from_url
from src.api.utils.sidejob import convert_income_level
from src.api.utils.politician import add_image_urls_to_politicians


def get_entity_by_id(db: Session, model, id: int):
    return db.query(model).filter(model.id == id).first()


def get_politicians_by_ids(db: Session, ids: List[int]):
    politicians = []
    for id in ids:
        politicians.append(get_entity_by_id(db, models.Politician, id))
    return add_image_urls_to_politicians(politicians)


def get_votes_and_polls_by_politician_id(
    db: Session, politician_id: int, range_of_votes: tuple, topic_ids: List[int] = None
):
    candidacy_mandate_ids = get_candidacy_mandate_ids_by_politician_id(
        db, politician_id
    )

    if topic_ids:
        votes_and_polls = (
            db.query(models.Vote, models.Poll)
            .filter(models.Vote.mandate_id.in_(candidacy_mandate_ids))
            .filter(models.Vote.poll_id == models.Poll.id)
            .filter(
                (models.Topic.id.in_(topic_ids))
                | (models.Topic.parent_id.in_(topic_ids))
            )
            .filter(
                (models.PollHasTopic.topic_id == models.Topic.id)
                & (models.Poll.id == models.PollHasTopic.poll_id)
            )
            .filter(models.Vote.vote != "no_show")
            .order_by(models.Poll.field_poll_date.desc())[
                range_of_votes[0] : range_of_votes[1]
            ]
        )
    else:
        votes_and_polls = (
            db.query(models.Vote, models.Poll)
            .filter(models.Vote.mandate_id.in_(candidacy_mandate_ids))
            .filter(models.Vote.poll_id == models.Poll.id)
            .filter(models.Vote.vote != "no_show")
            .order_by(models.Poll.field_poll_date.desc())[
                range_of_votes[0] : range_of_votes[1]
            ]
        )

    return votes_and_polls


def get_candidacy_mandate_ids_by_politician_id(db: Session, id: int) -> List[int]:
    data_list = []
    data = (
        db.query(models.CandidacyMandate.id)
        .filter(models.CandidacyMandate.politician_id == id)
        .all()
    )
    for datum in data:
        data_list.append(datum["id"])
    return data_list


def get_sidejobs_by_politician_id(db: Session, id: int):
    sidejobs = (
        db.query(models.Sidejob)
        .filter(models.Politician.id == id)
        .filter(models.Politician.id == models.CandidacyMandate.politician_id)
        .filter(
            models.CandidacyMandate.id == models.SidejobHasMandate.candidacy_mandate_id
        )
        .filter(models.SidejobHasMandate.sidejob_id == models.Sidejob.id)
        .all()
    )

    for item in sidejobs:
        item.__dict__["income_level"] = convert_income_level(
            item.__dict__["income_level"]
        )

    return sidejobs


def get_politicians_by_partial_name(db: Session, partial_name: str):
    return (
        db.query(models.Politician)
        .where(models.Politician.label.ilike(f"%{partial_name}%"))
        .all()
    )


def get_politicians_by_zipcode(db: Session, zipcode: int):
    politicians = (
        db.query(models.Politician)
        .filter(models.ZipCode.zip_code == str(zipcode))
        .filter(models.ElectoralData.constituency_id == models.ZipCode.constituency_id)
        .filter(models.CandidacyMandate.electoral_data_id == models.ElectoralData.id)
        .filter(models.Politician.id == models.CandidacyMandate.politician_id)
        .all()
    )

    return politicians


def get_politician_by_search(db: Session, search_text: str):
    try:
        zipcode = int(search_text)
        politicians = get_politicians_by_zipcode(db, zipcode)
    except ValueError:
        politicians = get_politicians_by_partial_name(db, search_text)

    return add_image_urls_to_politicians(politicians)


def get_politician_by_image_scanner(db: Session, search_text: str):
    politicians = get_politicians_by_partial_name(db, search_text)
    return add_image_urls_to_politicians(politicians)


# SELECT * FROM public.poll WHERE field_legislature_id = 111 or WHERE field_legislature_id = 132 ORDER by field_poll_date DESC
def get_latest_bundestag_polls(db: Session):
    return (
        db.query(models.Poll)
        .filter(
            or_(
                models.Poll.field_legislature_id == 111,
                models.Poll.field_legislature_id == 132,
            )
        )
        .order_by(models.Poll.field_poll_date.desc())
        .all()
    )


def get_polls_total(db: Session):
    data_list = []
    polls = get_latest_bundestag_polls(db)
    for poll in polls:
        poll_field_legislature_id = poll.field_legislature_id
        poll_id = poll.id
        poll_label = poll.label
        poll_field_poll_date = poll.field_poll_date
        result = (
            db.query(models.VoteResult)
            .filter(models.VoteResult.poll_id == poll_id)
            .first()
        )

        item_dict = {
            "poll_field_legislature_id": poll_field_legislature_id,
            "poll_id": poll_id,
            "poll_label": poll_label,
            "poll_field_poll_date": poll_field_poll_date,
            "result": result,
        }
        data_list.append(item_dict)
    return data_list


def get_poll_results_by_poll_id(db: Session, poll_id: int) -> list:
    return (
        db.query(models.PollResultPerFraction)
        .filter(models.PollResultPerFraction.poll_id == poll_id)
        .all()
    )


def get_politician_media(db: Session, abgeordnetenwatchID: int):
    raw_data = load_json_from_url(
        f"https://de.openparliament.tv/api/v1/search/media?abgeordnetenwatchID={abgeordnetenwatchID}"
    )

    if raw_data["meta"]["results"]["total"] == 0:
        return None

    media_list = []
    for item in raw_data["data"]:
        attributes = item["attributes"]
        media_item = {
            "videoFileURI": attributes["videoFileURI"],
            "creator": attributes["creator"],
            "timestamp": attributes["timestamp"],
            "dateStart": attributes["dateStart"],
            "dateEnd": attributes["dateEnd"],
        }
        media_list.append(media_item)

    sorted_media_list = sorted(media_list, key=lambda d: d["timestamp"], reverse=True)

    return sorted_media_list
