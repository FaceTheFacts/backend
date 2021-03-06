from operator import and_
from typing import List
import math
from unittest import result

# third-party
from sqlalchemy.orm import Session


# local
import src.db.models as models
from src.api.schemas import ConstituencyPoliticians
from src.api.utils.read_url import load_json_from_url
from src.api.utils.sidejob import convert_income_level
from src.api.utils.politician import (
    add_image_urls_to_politicians,
    transform_topics_dict_to_minimal_array,
    did_vote_pass,
)
from src.api.utils.topic_ids_converter import convert_into_topic_id
from src.api.utils.party_sort import party_sort


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
            db.query(models.Vote, models.Poll, models.VoteResult)
            .filter(models.Vote.mandate_id.in_(candidacy_mandate_ids))
            .filter(models.Vote.poll_id == models.Poll.id)
            .filter(models.VoteResult.poll_id == models.Poll.id)
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
            db.query(models.Vote, models.Poll, models.VoteResult)
            .filter(models.Vote.mandate_id.in_(candidacy_mandate_ids))
            .filter(models.Vote.poll_id == models.Poll.id)
            .filter(models.VoteResult.poll_id == models.Poll.id)
            .filter(models.Vote.vote != "no_show")
            .order_by(models.Poll.field_poll_date.desc())[
                range_of_votes[0] : range_of_votes[1]
            ]
        )

    for item in votes_and_polls:
        item[1].__dict__["poll_passed"] = did_vote_pass(item[-1].__dict__)

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


# Tested with mockup
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


def get_latest_sidejobs(db: Session):
    query_data = (
        db.query(models.Sidejob, models.Politician)
        .order_by(models.Sidejob.id.desc())
        .join(models.SidejobHasMandate)
        .join(models.CandidacyMandate)
        .join(models.Politician)
        .limit(5)
        .all()
    )
    sidejobs = []

    for query_object in query_data:
        query_object[0].__dict__["income_level"] = convert_income_level(
            query_object[0].__dict__["income_level"]
        )
        sidejob = {}
        sidejob["politician"] = query_object[1]
        sidejob["sidejob"] = query_object[0]
        sidejobs.append(sidejob)
    return sidejobs


def get_all_sidejobs(db: Session):
    query_data = (
        db.query(models.Sidejob, models.Politician)
        .order_by(models.Sidejob.id.desc())
        .join(models.SidejobHasMandate)
        .join(models.CandidacyMandate)
        .join(models.Politician)
        .limit(1000)
        .all()
    )
    sidejobs = []

    for query_object in query_data:
        query_object[0].__dict__["income_level"] = convert_income_level(
            query_object[0].__dict__["income_level"]
        )
        sidejob = {}
        sidejob["politician"] = query_object[1]
        sidejob["sidejob"] = query_object[0]
        sidejobs.append(sidejob)
    return sidejobs


def get_politicians_by_partial_name(db: Session, partial_name: str):
    return (
        db.query(models.Politician)
        .where(models.Politician.label.ilike(f"%{partial_name}%"))
        .all()[:20]
    )


def get_politicians_by_zipcode(db: Session, zipcode: int):
    politicians = (
        db.query(models.Politician)
        .filter(models.ZipCode.zip_code == str(zipcode))
        .filter(models.ElectoralData.constituency_id == models.ZipCode.constituency_id)
        .filter(models.CandidacyMandate.electoral_data_id == models.ElectoralData.id)
        .filter(models.Politician.id == models.CandidacyMandate.politician_id)
        .all()[:20]
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


# Tested with mockup
# SELECT * FROM public.poll WHERE field_legislature_id = 111 or WHERE field_legislature_id = 132 ORDER by field_poll_date DESC
def get_latest_bundestag_polls(db: Session):
    current_legislature_period = 132
    return (
        db.query(models.Poll)
        .filter(
            models.Poll.field_legislature_id == current_legislature_period,
        )
        .order_by(models.Poll.field_poll_date.desc())
        .limit(3)
        .all()
    )


def get_all_bundestag_polls(db: Session, size: int, topic_ids: List[int] = None):
    if topic_ids:
        return (
            db.query(models.Poll)
            .filter(
                (models.Poll.field_legislature_id == 111)
                | (models.Poll.field_legislature_id == 132)
            )
            .filter(
                (models.Topic.id.in_(topic_ids))
                | (models.Topic.parent_id.in_(topic_ids))
            )
            .filter(
                (models.PollHasTopic.topic_id == models.Topic.id)
                & (models.Poll.id == models.PollHasTopic.poll_id)
            )
            .order_by(models.Poll.field_poll_date.desc())
            .slice(size - 10, size)
            .all()
        )
    else:
        return (
            db.query(models.Poll)
            .filter(
                (models.Poll.field_legislature_id == 111)
                | (models.Poll.field_legislature_id == 132)
            )
            .order_by(models.Poll.field_poll_date.desc())
            .slice(size - 10, size)
            .all()
        )


# Tested with mockup
def get_vote_result_by_poll_id(db: Session, poll_id: int):
    return (
        db.query(models.VoteResult).filter(models.VoteResult.poll_id == poll_id).first()
    )


# Tested with mockup
def get_polls_total(db: Session):
    data_list = []
    polls = get_latest_bundestag_polls(db)
    for poll in polls:
        poll_dict = {
            "field_legislature_id": poll.field_legislature_id,
            "id": poll.id,
            "label": poll.label,
            "field_intro": poll.field_intro,
            "field_poll_date": poll.field_poll_date,
        }
        result_dict = get_vote_result_by_poll_id(db, poll.id)
        item_dict = {"poll": poll_dict, "result": result_dict}
        item_dict["poll"]["poll_passed"] = bool(
            result_dict.yes
            > 0.5
            * (
                result_dict.yes
                + result_dict.no
                + result_dict.abstain
                + result_dict.no_show
            )
        )
        data_list.append(item_dict)
    return data_list


def get_all_polls_total(db: Session, size: int, topic_ids: List[int] = None):
    data_list = []
    polls = get_all_bundestag_polls(db, size, topic_ids)
    for poll in polls:
        poll_dict = {
            "field_legislature_id": poll.field_legislature_id,
            "id": poll.id,
            "label": poll.label,
            "field_intro": poll.field_intro,
            "field_poll_date": poll.field_poll_date,
        }
        result_dict = get_vote_result_by_poll_id(
            db,
            poll.id,
        )
        item_dict = {"poll": poll_dict, "result": result_dict}
        item_dict["poll"]["poll_passed"] = bool(
            result_dict.yes
            > 0.5
            * (
                result_dict.yes
                + result_dict.no
                + result_dict.abstain
                + result_dict.no_show
            )
        )
        data_list.append(item_dict)
    return data_list


def get_poll_results_by_poll_id(db: Session, poll_id: int) -> list:
    return (
        db.query(models.PollResultPerFraction)
        .filter(models.PollResultPerFraction.poll_id == poll_id)
        .all()
    )


def get_poll_links_by_poll_id(db: Session, poll_id: int) -> list:
    return (
        db.query(models.FieldRelatedLink)
        .filter(models.FieldRelatedLink.poll_id == poll_id)
        .all()
    )


def get_votes_by_poll_id(db: Session, poll_id: int) -> dict:
    politician_votes = {}
    politician_votes["yes"] = (
        db.query(models.Politician)
        .join(models.CandidacyMandate)
        .join(models.Vote)
        .filter(and_(models.Vote.poll_id == poll_id, models.Vote.vote == "yes"))
        .all()
    )
    politician_votes["no"] = (
        db.query(models.Politician)
        .join(models.CandidacyMandate)
        .join(models.Vote)
        .filter(and_(models.Vote.poll_id == poll_id, models.Vote.vote == "no"))
        .all()
    )
    politician_votes["abstain"] = (
        db.query(models.Politician)
        .join(models.CandidacyMandate)
        .join(models.Vote)
        .filter(and_(models.Vote.poll_id == poll_id, models.Vote.vote == "abstain"))
        .all()
    )
    politician_votes["no_show"] = (
        db.query(models.Politician)
        .join(models.CandidacyMandate)
        .join(models.Vote)
        .filter(and_(models.Vote.poll_id == poll_id, models.Vote.vote == "no_show"))
        .all()
    )
    return politician_votes


def get_politician_speech(abgeordnetenwatch_id: int, page: int):
    raw_data = load_json_from_url(
        f"https://de.openparliament.tv/api/v1/search/media?abgeordnetenwatchID={abgeordnetenwatch_id}&page={page}&sort=date-desc"
    )

    total = raw_data["meta"]["results"]["total"]
    if total == 0:
        return None
    # openparliament.tv/api retrieves 10 data per a request
    last_page = math.ceil(total / 10)
    if last_page < page:
        return None

    speech_list = []
    for item in raw_data["data"]:
        attributes = item["attributes"]
        speech_item = {
            "videoFileURI": attributes["videoFileURI"],
            "title": item["relationships"]["agendaItem"]["data"]["attributes"]["title"],
            "date": attributes["dateStart"],
        }
        speech_list.append(speech_item)

    size = raw_data["meta"]["results"]["count"]
    is_last_page = last_page == page

    fetched_speeches = {
        "items": speech_list,
        "total": total,
        "page": page,
        "size": size,
        "is_last_page": is_last_page,
        "politician_id": abgeordnetenwatch_id,
    }
    return fetched_speeches


def get_bundestag_speech(db: Session, page: int):
    raw_data = load_json_from_url(
        f"https://de.openparliament.tv/api/v1/search/media?parliament=DE&page={page}&sort=date-desc"
    )

    total = raw_data["meta"]["results"]["total"]
    if total == 0:
        return None
    # openparliament.tv/api retrieves 10 data per a request
    last_page = math.ceil(total / 10)
    if last_page < page:
        return None
    speech_list = []
    for item in raw_data["data"]:
        attributes = item["attributes"]
        politician_id = item["relationships"]["people"]["data"][0]["attributes"][
            "additionalInformation"
        ]["abgeordnetenwatchID"]
        speech_item = {
            "videoFileURI": attributes["videoFileURI"],
            "title": item["relationships"]["agendaItem"]["data"]["attributes"]["title"],
            "date": attributes["dateStart"],
            "speaker": get_entity_by_id(db, models.Politician, int(politician_id)),
        }
        speech_list.append(speech_item)

    size = raw_data["meta"]["results"]["count"]
    is_last_page = last_page == page

    fetched_speeches = {
        "items": speech_list,
        "total": total,
        "page": page,
        "size": size,
        "is_last_page": is_last_page,
    }
    return fetched_speeches


def for_committee_topics__get_latest_parlament_period_id(db: Session, id: int):
    try:
        return (
            db.query(models.ParliamentPeriod.id)
            .filter(models.CandidacyMandate.politician_id == id)
            .filter(
                models.CandidacyMandate.parliament_period_id
                == models.ParliamentPeriod.id
            )
            .order_by(models.ParliamentPeriod.start_date_period.desc())
            .filter(models.ParliamentPeriod.id == models.Committee.field_legislature_id)
            .first()["id"]
        )
    except TypeError:
        return None


def get_topic_ids_by_field_legislature_id(
    db: Session, politician_id: int, field_legislature_id: int
):
    return (
        db.query(models.Topic.id, models.Topic.parent_id)
        .filter(models.CandidacyMandate.politician_id == politician_id)
        .filter(
            models.CommitteeMembership.candidacy_mandate_id
            == models.CandidacyMandate.id
        )
        .filter(models.CommitteeMembership.committee_id == models.Committee.id)
        .filter(models.Committee.field_legislature_id == field_legislature_id)
        .filter(models.Committee.id == models.CommitteeHasTopic.committee_id)
        .filter(models.CommitteeHasTopic.topic_id == models.Topic.id)
        .filter(models.Topic.id < 29)
        .distinct(models.Topic.id)
        .all()
    )


def get_latest_committee_topics_by_politician_id(db: Session, id: int) -> List:
    hardcoded_topic_id = convert_into_topic_id(id)
    if hardcoded_topic_id:
        return hardcoded_topic_id
    latest_parlament_period_id = for_committee_topics__get_latest_parlament_period_id(
        db, id
    )
    if latest_parlament_period_id:
        raw_topic_data = get_topic_ids_by_field_legislature_id(
            db, id, latest_parlament_period_id
        )
        if raw_topic_data:
            return transform_topics_dict_to_minimal_array(raw_topic_data)

    return []


def get_politician_by_constituency(
    db: Session, id: int
) -> ConstituencyPoliticians or None:
    constituency_politicians = {}
    candidacy_data = (
        db.query(models.CandidacyMandate)
        .filter(models.CandidacyMandate.politician_id == id)
        .filter(models.CandidacyMandate.type == "candidacy")
        .order_by(models.CandidacyMandate.id.desc())
        .first()
    )
    if candidacy_data:
        constituency_id = candidacy_data.electoral_data.constituency_id
        politicians = (
            db.query(models.Politician)
            .join(models.CandidacyMandate)
            .join(models.ElectoralData)
            .filter(models.ElectoralData.constituency_id == constituency_id)
            .all()
        )
        constituency = (
            db.query(models.Constituency)
            .filter(models.Constituency.id == constituency_id)
            .first()
        )
        constituency_politicians["constituency_number"] = constituency.number
        constituency_politicians["constituency_name"] = constituency.name
        constituency_politicians["politicians"] = party_sort(politicians)
        return constituency_politicians
    return None
