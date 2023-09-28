from operator import and_
from typing import List
import math
import datetime
from dateutil.relativedelta import relativedelta


# third-party
from sqlalchemy.orm import Session, joinedload

# local
import src.db.models as models
from src.api.schemas import ConstituencyPoliticians
from src.api.utils.sidejob import convert_income_level
from src.api.utils.politician import (
    add_image_urls_to_politicians,
    transform_topics_dict_to_minimal_array,
    did_vote_pass,
)
from src.api.utils.date_utils import get_last_day_of_the_month
from src.api.utils.topic_ids_converter import convert_into_topic_id
from src.api.utils.party_sort import party_sort
from src.api.utils.speeches import fetch_speech_data, process_speech_data


def get_entity_by_id(db: Session, model, id: int):
    return db.query(model).filter(model.id == id).first()


def get_politician_with_mandate_by_name(
    db: Session, name: str, parliament_period_id: int
):
    return (
        db.query(models.CandidacyMandate)
        .filter(models.CandidacyMandate.label.ilike(f"%{name}%"))
        .where(models.CandidacyMandate.parliament_period_id == parliament_period_id)
        .first()
    )


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
def get_sidejobs_by_politician_id(db: Session, id: int, version: str = "v2"):
    if version == "v1":
        sidejobs = (
            db.query(models.Sidejob)
            .filter(models.Politician.id == id)
            .filter(models.Politician.id == models.CandidacyMandate.politician_id)
            .filter(
                models.CandidacyMandate.id
                == models.SidejobHasMandate.candidacy_mandate_id
            )
            .filter(models.SidejobHasMandate.sidejob_id == models.Sidejob.id)
            .filter(models.Sidejob.id < 11701)
            .all()
        )
    else:
        sidejobs = (
            db.query(models.Sidejob)
            .filter(models.Politician.id == id)
            .filter(models.Politician.id == models.CandidacyMandate.politician_id)
            .filter(
                models.CandidacyMandate.id
                == models.SidejobHasMandate.candidacy_mandate_id
            )
            .filter(models.SidejobHasMandate.sidejob_id == models.Sidejob.id)
            .order_by(models.Sidejob.id.desc())
            .all()
        )

    for item in sidejobs:
        item.__dict__["income_level"] = convert_income_level(
            item.__dict__["income_level"]
        )

    return sidejobs


def get_latest_sidejobs(db: Session, version: str = "v2"):
    if version == "v1":
        query_data = (
            db.query(models.Sidejob, models.Politician)
            .filter(models.Sidejob.id < 11701)
            .order_by(models.Sidejob.id.desc())
            .join(models.SidejobHasMandate)
            .join(models.CandidacyMandate)
            .join(models.Politician)
            .limit(5)
            .all()
        )
    else:
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


def get_all_sidejobs(db: Session, version: str = "v2"):
    if version == "v1":
        query_data = (
            db.query(models.Sidejob, models.Politician)
            .filter(models.Sidejob.id < 11701)
            .order_by(models.Sidejob.id.desc())
            .join(models.SidejobHasMandate)
            .join(models.CandidacyMandate)
            .join(models.Politician)
            .limit(1000)
            .all()
        )
    else:
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


def get_bundestag_polls_by_topic(db: Session, topic_ids: List[int] = None):
    if topic_ids:
        return (
            db.query(models.Poll)
            .options(joinedload(models.Poll.vote_result))
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
            .all()
        )
    else:
        return (
            db.query(models.Poll)
            .options(joinedload(models.Poll.vote_result))
            .filter(
                (models.Poll.field_legislature_id == 111)
                | (models.Poll.field_legislature_id == 132)
            )
            .order_by(models.Poll.field_poll_date.desc())
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


def get_politician_speech(
    db: Session, abgeordnetenwatch_id: int, page: int, plugin: bool = False
):
    raw_data = fetch_speech_data(page, abgeordnetenwatch_id)
    if raw_data is None:
        return None

    fetched_speeches = process_speech_data(
        db=db,
        get_entity_by_id_func=get_entity_by_id,
        get_politician_with_mandate_by_name_func=get_politician_with_mandate_by_name,
        page=page,
        raw_data=raw_data,
        abgeordnetenwatch_id=abgeordnetenwatch_id,
        plugin=plugin,
    )
    return fetched_speeches


def get_bundestag_speech(db: Session, page: int, plugin: bool = False):
    raw_data = fetch_speech_data(page)

    if not raw_data:
        return None

    fetched_speeches = process_speech_data(
        db=db,
        get_entity_by_id_func=get_entity_by_id,
        get_politician_with_mandate_by_name_func=get_politician_with_mandate_by_name,
        page=page,
        raw_data=raw_data,
        plugin=plugin,
    )

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

        if constituency_id not in [9607, 4721, 5309, 423]:
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


def get_party_donations_sorted_by_party_and_date(
    db: Session,
    party_ids: list,
    start_of_time_range: datetime,
    end_of_time_range: datetime,
):
    if end_of_time_range < start_of_time_range:
        raise ValueError("End of time range cannot be before start of time range")

    sorted_donations = (
        db.query(models.PartyDonation)
        .filter(models.PartyDonation.party_id.in_(party_ids))
        .filter(models.PartyDonation.date >= start_of_time_range)
        .filter(models.PartyDonation.date < end_of_time_range)
        .order_by(models.PartyDonation.party_id, models.PartyDonation.date.desc())
    )

    for donation in sorted_donations.all():
        print(donation.party_id, donation.date.strftime("%m/%d/%Y"))

    # prints ordered by party ID and desc date, e.g.:
    # 3 12/18/2015
    # 4 12/22/2021
    # 5 05/27/2022
    # 5 05/19/2022

    # use itertools.groupby() to group by dynamic date ranges?

    return sorted_donations


def get_party_donations_for_ids_and_time_range(
    db: Session,
    party_ids: list,
    start_of_time_range: datetime,
    end_of_time_range: datetime,
):
    if end_of_time_range < start_of_time_range:
        raise ValueError("End of time range cannot be before start of time range")

    return (
        db.query(models.PartyDonation)
        .filter(models.PartyDonation.party_id.in_(party_ids))
        .filter(models.PartyDonation.date >= start_of_time_range)
        .filter(models.PartyDonation.date < end_of_time_range)
        .order_by(models.PartyDonation.date.asc())
        .all()
    )


def build_donation_data_response_object(bundestag_party_ids: list):
    response_donation_data_container = []

    for party_id in bundestag_party_ids:
        data = {
            "id": party_id,
            "party": None,
            "donations_over_32_quarters": [],
            "donations_total": 0,
            "largest_quarter": None,
        }
        response_donation_data_container.append(data)

    return response_donation_data_container


def build_donations_over_time_container(bundestag_party_ids: list, quarters: int):
    donations_over_quarters = {}

    for party_id in bundestag_party_ids:
        donations_over_quarters[party_id] = [0] * quarters

    return donations_over_quarters


def get_parties_by_id(db: Session, party_ids: list):
    return db.query(models.Party).filter(models.Party.id.in_(party_ids))


def add_party_data_to_donations_response(
    bundestag_parties_query: list, response_donation_data: list
):
    for db_party in bundestag_parties_query:
        for party in response_donation_data:
            if party["id"] == db_party.id:
                party["party"] = db_party
                continue

    return response_donation_data


def delete_excess_party_data(response_donation_data):
    for party in response_donation_data:
        del party["id"]

    return response_donation_data


def get_homepage_party_donations(db: Session, bundestag_party_ids: list):
    date_8_years_ago_today = datetime.datetime.now() - relativedelta(years=8)

    bundestag_party_donations_last_8_years_query = (
        get_party_donations_for_ids_and_time_range(
            db, bundestag_party_ids, date_8_years_ago_today, datetime.datetime.now()
        )
    )

    response_donation_data = build_donation_data_response_object(bundestag_party_ids)
    donations_over_32_quarters = build_donations_over_time_container(
        bundestag_party_ids, 32
    )

    bundestag_parties_query = get_parties_by_id(db, bundestag_party_ids)

    response_donation_data = add_party_data_to_donations_response(
        bundestag_parties_query, response_donation_data
    )

    # assign donations to their respective parties
    for donation in bundestag_party_donations_last_8_years_query:
        donation_time_from_beginning_of_range = relativedelta(
            donation.date, date_8_years_ago_today
        )

        # Every year is 4 quarters, the remaining months can be calculated as quarters
        months = donation_time_from_beginning_of_range.months
        additional_quarters = 0

        if months <= 2:
            additional_quarters = 0
        elif months >= 3 and months <= 5:
            additional_quarters = 1
        elif months >= 6 and months <= 8:
            additional_quarters = 2
        else:
            additional_quarters = 3

        donation_quarter_index = (
            donation_time_from_beginning_of_range.years * 4
        ) + additional_quarters

        donations_over_32_quarters[donation.party_id][
            donation_quarter_index
        ] += donation.amount

    for party in response_donation_data:
        party["donations_over_32_quarters"] = donations_over_32_quarters[party["id"]]
        party["donations_total"] = sum(donations_over_32_quarters[party["id"]])
        party["largest_quarter"] = max(donations_over_32_quarters[party["id"]])

    # remove excess data from response object to match schema
    response_donation_data = delete_excess_party_data(response_donation_data)

    return response_donation_data


class PartyDonationResponse:
    def __init__(
        self, party_ids: list, time_range_start: datetime, time_range_end: datetime
    ):
        self.party_ids = party_ids
        self.time_range_start = time_range_start
        self.time_range_end = time_range_end


def get_all_party_donations(db: Session, party_ids: list = None):
    if party_ids:
        party_donations = (
            db.query(models.PartyDonation)
            .filter(models.PartyDonation.party_id.in_(party_ids))
            .order_by(models.PartyDonation.date.desc())
            .all()
        )
    else:
        party_donations = (
            db.query(models.PartyDonation)
            .order_by(models.PartyDonation.date.desc())
            .all()
        )

    return party_donations


def get_topics(db: Session):
    topics = db.query(models.Topic).all()

    return topics


def get_parties(db: Session):
    parties = db.query(models.Party).order_by(models.Party.id.asc()).all()

    return parties


def get_party_donations_details(db: Session):
    # get all party donations sorted by party id, then by date, in ascending order
    party_donations = (
        db.query(models.PartyDonation)
        .order_by(models.PartyDonation.party_id.asc(), models.PartyDonation.date.asc())
        .all()
    )

    response_data = {}
    last_day_of_the_month = get_last_day_of_the_month()
    four_years_ago_from_end_of_month = last_day_of_the_month - relativedelta(years=4)

    eight_years_ago_from_end_of_month = last_day_of_the_month - relativedelta(years=8)

    # for every donation, add it to the response object as a dictionary using the party id as the key, and separate the donations into three groups: the last 4 years, the last 8 years, and all time
    for donation in party_donations:
        # if a is not yet in the response object, add it, along with party info and date ranges
        if str(donation.party_id) not in response_data:
            response_data[str(donation.party_id)] = {
                "donations_older_than_8_years": [],
                "donations_4_to_8_years_old": [],
                "donations_less_than_4_years_old": [],
            }

        # add donation to the appropriate date range for its party
        if donation.date < eight_years_ago_from_end_of_month:
            response_data[str(donation.party_id)][
                "donations_older_than_8_years"
            ].append(donation)
        elif donation.date < four_years_ago_from_end_of_month:
            response_data[str(donation.party_id)]["donations_4_to_8_years_old"].append(
                donation
            )
        else:
            response_data[str(donation.party_id)][
                "donations_less_than_4_years_old"
            ].append(donation)

    return response_data
