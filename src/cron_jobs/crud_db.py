# std
import time
import unicodedata

# local
from src.cron_jobs.utils.file import has_valid_file, read_json, write_json
from src.cron_jobs.utils.fetch import (
    fetch_entity,
    fetch_json,
    load_entity,
    load_entity_from_db,
)
from src.db.connection import engine, Session, Base
from src.db.models.country import Country
from src.db.models.city import City
from src.db.models.party_style import PartyStyle
from src.db.models.party import Party
from src.db.models.politician import Politician
from src.db.models.parliament import Parliament
from src.db.models.parliament_period import ParliamentPeriod
from src.db.models.topic import Topic
from src.db.models.committee import Committee
from src.db.models.committee_has_topic import CommitteeHasTopic
from src.db.models.fraction import Fraction
from src.db.models.constituency import Constituency
from src.db.models.electoral_list import ElectoralList
from src.db.models.election_program import ElectionProgram
from src.db.models.fraction_membership import FractionMembership
from src.db.models.electoral_data import ElectoralData
from src.db.models.candidacy_mandate import CandidacyMandate
from src.db.models.committee_membership import CommitteeMembership
from src.db.models.poll import Poll
from src.db.models.poll_has_topic import PollHasTopic
from src.db.models.field_related_link import FieldRelatedLink
from src.db.models.vote import Vote
from src.db.models.sidejob_organization import SidejobOrganization
from src.db.models.sidejob_organization_has_topic import SidejobOrganizationHasTopic
from src.db.models.sidejob import Sidejob
from src.db.models.sidejob_has_mandate import SidejobHasMandate
from src.db.models.sidejob_has_topic import SidejobHasTopic
from src.db.models.position_statement import PositionStatement
from src.db.models.cv import CV
from src.db.models.career_path import CareerPath
from src.db.models.position import Position
from src.db.models.politician_weblink import PoliticianWeblink
from src.db.models.poll_result_per_party import PollResultPerFraction

import src.db.models as models
from src.cron_jobs.utils.vote_result import (
    generate_vote_results,
    get_total_votes_of_type,
)
from src.cron_jobs.utils.insert_and_update import insert_and_update
from src.cron_jobs.utils.parser import (
    gen_statements,
    gen_positions,
    gen_party_styles_map,
    PERIOD_POSITION_TABLE,
)
from src.cron_jobs.utils.truncate_table import truncate_table

# third-party
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func

session = Session()


def populate_countries() -> None:
    api_countries = load_entity("countries")
    countries = [
        {
            "id": api_country["id"],
            "entity_type": api_country["entity_type"],
            "label": api_country["label"],
            "api_url": api_country["api_url"],
        }
        for api_country in api_countries
    ]
    insert_and_update(Country, countries)


def populate_cities() -> None:
    api_cities = load_entity("cities")
    cities = [
        {
            "id": api_city["id"],
            "entity_type": api_city["entity_type"],
            "label": api_city["label"],
            "api_url": api_city["api_url"],
        }
        for api_city in api_cities
    ]
    insert_and_update(City, cities)


def populate_party_styles() -> None:
    api_parties = load_entity("parties")
    party_styles_map = gen_party_styles_map(api_parties)
    party_styles = []
    for api_party in api_parties:
        party_id: int = api_party["id"]
        if party_id in party_styles_map:
            party_styles.append(party_styles_map[party_id])
        else:
            party_style = {
                "id": party_id,
                "display_name": api_party["label"],
                "foreground_color": "#FFFFFF",
                "background_color": "#333333",
                "border_color": None,
            }
            party_styles.append(party_style)
    insert_and_update(PartyStyle, party_styles)


def populate_parties() -> None:
    api_parties = load_entity("parties")
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
        for api_party in api_parties
    ]
    insert_and_update(Party, parties)


def populate_politicians() -> None:
    api_politicians = load_entity("politicians")
    begin_time = time.time()
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
        for api_politician in api_politicians
    ]
    insert_and_update(Politician, politicians)
    end_time = time.time()
    print(
        f"Total runtime to store {len(api_politicians)} data is {end_time - begin_time}"
    )


def populate_parliaments() -> None:
    api_parliaments = load_entity("parliaments")
    parliaments = [
        {
            "id": api_parliament["id"],
            "entity_type": api_parliament["entity_type"],
            "label": api_parliament["label"],
            "api_url": api_parliament["api_url"],
            "abgeordnetenwatch_url": api_parliament["abgeordnetenwatch_url"],
            "label_external_long": api_parliament["label_external_long"],
        }
        for api_parliament in api_parliaments
    ]
    insert_and_update(Parliament, parliaments)


def update_parliament_current_project_ids() -> None:
    api_parliaments = load_entity("parliaments")
    parliaments = [
        {
            "id": parliament["id"],
            "current_project_id": parliament["current_project"]["id"]
            if parliament["current_project"]
            else None,
        }
        for parliament in api_parliaments
    ]

    for parliament in parliaments:
        if parliament["current_project_id"]:
            engine.execute(
                "UPDATE {table} SET current_project_id = {current_project_id} WHERE id = {id}".format(
                    table=Parliament.__tablename__,
                    current_project_id=parliament["current_project_id"],
                    id=parliament["id"],
                )
            )


def populate_parliament_periods() -> None:
    api_parliament_periods = load_entity("parliament-periods")
    parliament_periods = [
        {
            "id": api_parliament_period["id"],
            "entity_type": api_parliament_period["entity_type"],
            "label": api_parliament_period["label"],
            "api_url": api_parliament_period["api_url"],
            "abgeordnetenwatch_url": api_parliament_period["abgeordnetenwatch_url"],
            "type": api_parliament_period["type"],
            "election_date": api_parliament_period["election_date"],
            "start_date_period": api_parliament_period["start_date_period"],
            "end_date_period": api_parliament_period["end_date_period"],
            "parliament_id": api_parliament_period["parliament"]["id"]
            if api_parliament_period["parliament"]
            else None,
            "previous_period_id": api_parliament_period["previous_period"]["id"]
            if api_parliament_period["previous_period"]
            else None,
        }
        for api_parliament_period in api_parliament_periods
    ]
    parliament_periods = sorted(parliament_periods, key=lambda p: p["id"])
    insert_and_update(ParliamentPeriod, parliament_periods)
    update_parliament_current_project_ids()


def populate_topics() -> None:
    api_topics = load_entity("topics")
    topics = [
        {
            "id": api_topic["id"],
            "entity_type": api_topic["entity_type"],
            "label": api_topic["label"],
            "api_url": api_topic["api_url"],
            "abgeordnetenwatch_url": api_topic["abgeordnetenwatch_url"],
            "description": api_topic["description"],
            "parent_id": api_topic["parent"][0]["id"] if api_topic["parent"] else None,
        }
        for api_topic in api_topics
    ]
    topics = sorted(topics, key=lambda t: t["id"])
    insert_and_update(Topic, topics)


def populate_committees() -> None:
    api_committees = load_entity("committees")
    committees = [
        {
            "id": api_committee["id"],
            "entity_type": api_committee["entity_type"],
            "label": api_committee["label"],
            "api_url": api_committee["api_url"],
            "field_legislature_id": api_committee["field_legislature"]["id"],
        }
        for api_committee in api_committees
    ]
    insert_and_update(Committee, committees)


def populate_committee_has_topic() -> None:
    api_committees = load_entity("committees")
    committee_topics = []
    for api_committee in api_committees:
        field_topics = api_committee["field_topics"]
        if field_topics:
            for topic in field_topics:
                committee_topic = {
                    "committee_id": api_committee["id"],
                    "topic_id": topic["id"],
                }
                committee_topics.append(committee_topic)
    stmt = insert(CommitteeHasTopic).values(committee_topics)
    stmt = stmt.on_conflict_do_nothing()
    session = Session()
    session.execute(stmt)
    session.commit()
    session.close()


def populate_fractions() -> None:
    api_fractions = load_entity("fractions")
    fractions = [
        {
            "id": api_fraction["id"],
            "entity_type": api_fraction["entity_type"],
            "label": api_fraction["label"],
            "api_url": api_fraction["api_url"],
            "full_name": api_fraction["full_name"],
            "short_name": api_fraction["short_name"],
            "legislature_id": api_fraction["legislature"]["id"]
            if api_fraction["legislature"]
            else None,
        }
        for api_fraction in api_fractions
    ]
    insert_and_update(Fraction, fractions)


def populate_constituencies() -> None:
    api_constituencies = load_entity("constituencies")
    constituencies = [
        {
            "id": api_constituency["id"],
            "entity_type": api_constituency["entity_type"],
            "label": api_constituency["label"],
            "api_url": api_constituency["api_url"],
            "name": api_constituency["name"],
            "number": api_constituency["number"],
        }
        for api_constituency in api_constituencies
    ]
    insert_and_update(Constituency, constituencies)


def update_constituencies_with_parliament_period_id() -> None:
    begin_time = time.time()
    constituencies = []
    constituency_dict = {}

    api_constituencies = load_entity("constituencies")
    for item in api_constituencies:
        constituency_dict[item["id"]] = item

    json_data = read_json(
        "src/data_scraper/json_data/constituency_id_parliament_period_id.json"
    )

    for item in json_data:
        constituency_id = item["constituency_id"]
        has_api_constituency = constituency_dict.get(constituency_id)

        if has_api_constituency:
            api_constituency = constituency_dict[constituency_id]
            constituency = {
                "id": api_constituency["id"],
                "entity_type": api_constituency["entity_type"],
                "label": api_constituency["label"],
                "api_url": api_constituency["api_url"],
                "name": api_constituency["name"],
                "number": api_constituency["number"],
                # Add parliament_period_id from json
                "parliament_period_id": item["parliament_period_id"],
            }

            constituencies.append(constituency)
    insert_and_update(Constituency, constituencies)
    end_time = time.time()
    print(f"Total runtime to store {len(json_data)} data is {end_time - begin_time}")


def populate_electoral_lists() -> None:
    api_electoral_lists = load_entity("electoral-lists")
    electoral_lists = [
        {
            "id": api_electoral_list["id"],
            "entity_type": api_electoral_list["entity_type"],
            "label": api_electoral_list["label"],
            "api_url": api_electoral_list["api_url"],
            "name": api_electoral_list["name"],
            "parliament_period_id": api_electoral_list["parliament_period"]["id"]
            if api_electoral_list["parliament_period"]
            else None,
        }
        for api_electoral_list in api_electoral_lists
    ]
    insert_and_update(ElectoralList, electoral_lists)


def populate_election_programs() -> None:
    api_election_programs = load_entity("election-program")
    election_programs = [
        {
            "id": api_election_program["id"],
            "entity_type": api_election_program["entity_type"],
            "label": api_election_program["label"],
            "api_url": api_election_program["api_url"],
            "parliament_period_id": api_election_program["parliament_period"]["id"]
            if api_election_program["parliament_period"]
            else None,
            "party_id": api_election_program["party"]["id"]
            if api_election_program["party"]
            else None,
            "link_uri": api_election_program["link"][0]["uri"],
            "link_title": api_election_program["link"][0]["title"],
            "link_option": api_election_program["link"][0]["option"]
            if api_election_program["link"][0].get("option")
            else None,
            "file": api_election_program["file"],
        }
        for api_election_program in api_election_programs
    ]
    insert_and_update(ElectionProgram, election_programs)


def populate_fraction_memberships() -> None:
    api_candidacies_mandates = load_entity("candidacies-mandates")
    fraction_memberships = []
    for api_candidacies_mandate in api_candidacies_mandates:
        fraction_membership = api_candidacies_mandate.get("fraction_membership")
        if fraction_membership:
            membership = fraction_membership[0]
            new_fraction_membership = {
                "id": membership["id"],
                "entity_type": membership["entity_type"],
                "label": membership["label"],
                "fraction_id": membership["fraction"]["id"],
                "valid_from": membership["valid_from"],
                "valid_until": membership["valid_until"],
            }
            fraction_memberships.append(new_fraction_membership)
    insert_and_update(FractionMembership, fraction_memberships)


def populate_electoral_data() -> None:
    api_candidacies_mandates = load_entity("candidacies-mandates")
    electoral_data_list = []
    for api_candidacies_mandate in api_candidacies_mandates:
        electoral_data = api_candidacies_mandate["electoral_data"]
        if electoral_data:
            new_electoral_data = {
                "id": electoral_data["id"],
                "entity_type": electoral_data["entity_type"],
                "label": electoral_data["label"],
                "electoral_list_id": electoral_data["electoral_list"]["id"]
                if electoral_data["electoral_list"]
                else None,
                "list_position": electoral_data["list_position"],
                "constituency_id": electoral_data["constituency"]["id"]
                if electoral_data["constituency"]
                else None,
                "constituency_result": electoral_data["constituency_result"],
                "constituency_result_count": electoral_data[
                    "constituency_result_count"
                ],
                "mandate_won": electoral_data["mandate_won"],
            }
            electoral_data_list.append(new_electoral_data)
    insert_and_update(ElectoralData, electoral_data_list)


def populate_candidacies_mandates() -> None:
    api_candidacies_mandates = load_entity("candidacies-mandates")
    begin_time = time.time()
    candidacies_mandates = [
        {
            "id": api_candidacies_mandate["id"],
            "entity_type": api_candidacies_mandate["entity_type"],
            "label": api_candidacies_mandate["label"],
            "api_url": api_candidacies_mandate["api_url"],
            "id_external_administration": api_candidacies_mandate[
                "id_external_administration"
            ],
            "id_external_administration_description": api_candidacies_mandate[
                "id_external_administration_description"
            ],
            "type": api_candidacies_mandate["type"],
            "parliament_period_id": api_candidacies_mandate["parliament_period"]["id"]
            if api_candidacies_mandate["parliament_period"]
            else None,
            "politician_id": api_candidacies_mandate["politician"]["id"]
            if api_candidacies_mandate["politician"]
            else None,
            # Some dict don't include party itsself
            "party_id": api_candidacies_mandate["party"]["id"]
            if api_candidacies_mandate.get("party")
            else None,
            "start_date": api_candidacies_mandate["start_date"],
            "end_date": api_candidacies_mandate["end_date"],
            "info": api_candidacies_mandate["info"],
            "electoral_data_id": api_candidacies_mandate["electoral_data"]["id"]
            if api_candidacies_mandate["electoral_data"]
            else None,
            # Some dict don't include fraction_membership itsself
            "fraction_membership_id": api_candidacies_mandate["fraction_membership"][0][
                "id"
            ]
            if api_candidacies_mandate.get("fraction_membership")
            else None,
        }
        for api_candidacies_mandate in api_candidacies_mandates
    ]
    insert_and_update(CandidacyMandate, candidacies_mandates)
    end_time = time.time()
    print(
        f"Total runtime to store {len(candidacies_mandates)} data is {end_time - begin_time}"
    )


def populate_committee_memberships() -> None:
    api_committees = load_entity("committees")
    committee_ids = set([api_committee["id"] for api_committee in api_committees])
    api_committee_memberships = load_entity("committee-memberships")
    begin_time = time.time()
    committee_memberships = []
    for api_committee_membership in api_committee_memberships:
        committee_id = (
            api_committee_membership["committee"]["id"]
            if api_committee_membership["committee"]
            else None
        )
        if committee_id in committee_ids:
            new_membership = {
                "id": api_committee_membership["id"],
                "entity_type": api_committee_membership["entity_type"],
                "label": api_committee_membership["label"],
                "api_url": api_committee_membership["api_url"],
                "committee_id": api_committee_membership["committee"]["id"]
                if api_committee_membership["committee"]
                else None,
                "candidacy_mandate_id": api_committee_membership["candidacy_mandate"][
                    "id"
                ]
                if api_committee_membership["candidacy_mandate"]
                else None,
                "committee_role": api_committee_membership["committee_role"],
            }
            committee_memberships.append(new_membership)
    insert_and_update(CommitteeMembership, committee_memberships)
    end_time = time.time()
    print(
        f"Total runtime to store {len(committee_memberships)} data is {end_time - begin_time}"
    )


def populate_polls() -> None:
    api_polls = load_entity("polls")
    polls = [
        {
            "id": api_polls["id"],
            "entity_type": api_polls["entity_type"],
            "label": api_polls["label"],
            "api_url": api_polls["api_url"],
            "field_committees_id": api_polls["field_committees"][0]["id"]
            if api_polls["field_committees"]
            else None,
            "field_intro": api_polls["field_intro"]
            if api_polls["field_intro"]
            else None,
            "field_legislature_id": api_polls["field_legislature"]["id"]
            if api_polls["field_legislature"]
            else None,
            "field_poll_date": api_polls["field_poll_date"],
        }
        for api_polls in api_polls
    ]
    insert_and_update(Poll, polls)


def populate_poll_has_topic() -> None:
    api_polls = load_entity("polls")
    polls_topics = []
    for api_poll in api_polls:
        field_topics = api_poll["field_topics"]
        if field_topics:
            for topic in field_topics:
                poll_topic = {
                    "poll_id": api_poll["id"],
                    "topic_id": topic["id"],
                }
                polls_topics.append(poll_topic)
    session = Session()
    stmt = insert(PollHasTopic).values(polls_topics)
    stmt = stmt.on_conflict_do_nothing()
    session.execute(stmt)
    session.commit()
    session.close()


def populate_field_related_link() -> None:
    api_polls = load_entity("polls")
    poll_related_links = []
    for api_poll in api_polls:
        poll_id = api_poll["id"]
        field_related_links = api_poll["field_related_links"]
        if field_related_links:
            for field_related_link in field_related_links:
                poll_related_link = {
                    "poll_id": poll_id,
                    "uri": field_related_link["uri"],
                    "title": field_related_link["title"],
                }
                poll_related_links.append(poll_related_link)
    insert_and_update(FieldRelatedLink, poll_related_links)


def populate_votes() -> None:
    api_polls = load_entity("polls")
    poll_ids = set([api_poll["id"] for api_poll in api_polls])
    api_votes = load_entity("votes")
    begin_time = time.time()
    votes = []
    for api_vote in api_votes:
        poll_id = api_vote["poll"]["id"] if api_vote["poll"] else None
        if poll_id in poll_ids:
            vote = {
                "id": api_vote["id"],
                "entity_type": api_vote["entity_type"],
                "label": api_vote["label"],
                "api_url": api_vote["api_url"],
                "mandate_id": api_vote["mandate"]["id"]
                if api_vote["mandate"]
                else None,
                "fraction_id": api_vote["fraction"]["id"]
                if api_vote["fraction"]
                else None,
                "poll_id": poll_id,
                "vote": api_vote["vote"],
                "reason_no_show": api_vote["reason_no_show"],
                "reason_no_show_other": api_vote["reason_no_show_other"],
            }
            votes.append(vote)
    insert_and_update(Vote, votes)
    end_time = time.time()
    print(f"Total runtime to store {len(api_votes)} data is {end_time - begin_time}")


# id=1 to id=281 are missing
def complement_missing_votes():
    api_polls = load_entity("polls")
    poll_ids = set([api_poll["id"] for api_poll in api_polls])
    api_votes = list(
        (
            fetch_json(
                "https://www.abgeordnetenwatch.de/api/v2/votes?id[lt]=282&range_end=1000"
            )["data"]
        )
    )
    votes = []
    for api_vote in api_votes:
        poll_id = api_vote["poll"]["id"] if api_vote["poll"] else None
        if poll_id in poll_ids:
            vote = {
                "id": api_vote["id"],
                "entity_type": api_vote["entity_type"],
                "label": api_vote["label"],
                "api_url": api_vote["api_url"],
                "mandate_id": api_vote["mandate"]["id"]
                if api_vote["mandate"]
                else None,
                "fraction_id": api_vote["fraction"]["id"]
                if api_vote["fraction"]
                else None,
                "poll_id": poll_id,
                "vote": api_vote["vote"],
                "reason_no_show": api_vote["reason_no_show"],
                "reason_no_show_other": api_vote["reason_no_show_other"],
            }
            votes.append(vote)
    insert_and_update(Vote, votes)


def populate_sidejob_organizations() -> None:
    api_sidejob_organizations = load_entity("sidejob-organizations")
    sidejob_organizations = [
        {
            "id": api_sidejob_organization["id"],
            "entity_type": api_sidejob_organization["entity_type"],
            "label": api_sidejob_organization["label"],
            "api_url": api_sidejob_organization["api_url"],
            "field_city_id": api_sidejob_organization["field_city"]["id"]
            if api_sidejob_organization["field_city"]
            else None,
            "field_country_id": api_sidejob_organization["field_country"]["id"]
            if api_sidejob_organization["field_country"]
            else None,
        }
        for api_sidejob_organization in api_sidejob_organizations
    ]
    insert_and_update(SidejobOrganization, sidejob_organizations)


def populate_sidejob_organization_has_topic() -> None:
    api_sidejob_organizations = load_entity("sidejob-organizations")
    organization_topics = []
    for api_sidejob_organization in api_sidejob_organizations:
        field_topics = api_sidejob_organization["field_topics"]
        if field_topics:
            for topic in field_topics:
                organization_topic = {
                    "sidejob_organization_id": api_sidejob_organization["id"],
                    "topic_id": topic["id"],
                }
                organization_topics.append(organization_topic)
    session = Session()
    stmt = insert(SidejobOrganizationHasTopic).values(organization_topics)
    stmt = stmt.on_conflict_do_nothing()
    session.execute(stmt)
    session.commit()
    session.close()


def populate_sidejobs() -> None:
    api_sidejobs = load_entity("sidejobs")
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
        for api_sidejob in api_sidejobs
    ]
    insert_and_update(Sidejob, sidejobs)


def populate_sidejob_has_mandate() -> None:
    api_sidejobs = load_entity("sidejobs")
    sidejob_mandates = []
    for api_sidejob in api_sidejobs:
        mandates = api_sidejob["mandates"]
        if mandates:
            for mandate in mandates:
                sidejob_mandate = {
                    "sidejob_id": api_sidejob["id"],
                    "candidacy_mandate_id": mandate["id"],
                }
                sidejob_mandates.append(sidejob_mandate)
    stmt = insert(SidejobHasMandate).values(sidejob_mandates)
    stmt = stmt.on_conflict_do_nothing()
    session = Session()
    session.execute(stmt)
    session.commit()
    session.close()


def populate_sidejob_has_topic() -> None:
    api_sidejobs = load_entity("sidejobs")
    sidejob_topics = []
    for api_sidejob in api_sidejobs:
        field_topics = api_sidejob["field_topics"]
        if field_topics:
            for topic in field_topics:
                sidejob_topic = {
                    "sidejob_id": api_sidejob["id"],
                    "topic_id": topic["id"],
                }
                sidejob_topics.append(sidejob_topic)
    stmt = insert(SidejobHasTopic).values(sidejob_topics)
    stmt = stmt.on_conflict_do_nothing()
    session = Session()
    session.execute(stmt)
    session.commit()
    session.close()


def populate_position_statements() -> None:
    position_statements = []
    for period_id in PERIOD_POSITION_TABLE:
        statements = gen_statements(period_id)
        position_statements += statements
    insert_and_update(PositionStatement, position_statements)


def populate_positions() -> None:
    positions_list = []
    for period_id in PERIOD_POSITION_TABLE:
        positions = gen_positions(period_id)
        positions_list += positions
    insert_and_update(Position, positions_list)


def populate_cvs_and_career_paths() -> None:
    cv_connection = read_json("src/cron_jobs/data/220516_connections.json")
    cv_table = load_entity_from_db(models.CV)
    cv_table_ids = [cv.politician_id for cv in cv_table]
    last_cv_id = 755
    cvs = []
    for politician in cv_connection:
        id = politician["ID"]
        cv_data = read_json(f"src/cron_jobs/data/data_politicians/{id}.json")
        if id in cv_table_ids:
            for cv in cv_table:
                if cv.politician_id == id:
                    cv = {
                        "id": cv.id,
                        "politician_id": id,
                        "raw_text": unicodedata.normalize(
                            "NFKD", cv_data["Biography"]["Raw"]
                        ),
                        "short_description": unicodedata.normalize(
                            "NFKD", cv_data["Biography"]["ShortDescription"]
                        ),
                    }
                    cvs.append(cv)
        else:
            cv = {
                "id": last_cv_id,
                "politician_id": id,
                "raw_text": unicodedata.normalize("NFKD", cv_data["Biography"]["Raw"]),
                "short_description": unicodedata.normalize(
                    "NFKD", cv_data["Biography"]["ShortDescription"]
                ),
            }
            cvs.append(cv)
            last_cv_id += 1
    write_json("src/cron_jobs/data/cvs_new.json", cvs)
    # insert_and_update(CV, cvs)


def insert_cv() -> None:
    cv_connection = read_json("src/cron_jobs/data/220516_connections.json")
    weblink_table = load_entity_from_db(models.PoliticianWeblink)
    cv_table_ids = [cv.politician_id for cv in weblink_table]
    last_cv_id = 1
    weblinks = []
    for politician in cv_connection:
        id = politician["ID"]
        cv_data = read_json(f"src/cron_jobs/data/data_politicians/{id}.json")
        if id not in cv_table_ids:
            bundestagLink = {
                "id": last_cv_id,
                "politician_id": id,
                "link": cv_data["Href"],
            }
            weblinks.append(bundestagLink)
            last_cv_id += 1
            if "Links" in cv_data:
                for link in cv_data["Links"]:
                    new_link = {
                        "id": last_cv_id,
                        "politician_id": id,
                        "link": link,
                    }
                    weblinks.append(new_link)
                    last_cv_id += 1
            else:
                print("No links")
                print(id)
    write_json("src/cron_jobs/data/weblinks_new.json", weblinks)
    insert_and_update(PoliticianWeblink, weblinks)
    # cvs = read_json("src/cron_jobs/data/cvs_new.json")
    # insert_and_update(CV, cvs)


def populate_weblinks() -> None:
    truncate_table("politician_weblink")
    weblink_data = read_json("src/data_scraper/json_data/weblinks.json")
    weblinks = []
    for item in weblink_data:
        links = item["weblink"]
        for link in links:
            weblink = {
                "politician_id": item["politician_id"],
                "link": link,
            }
            weblinks.append(weblink)
    insert_and_update(PoliticianWeblink, weblinks)


def populate_vote_result() -> None:
    vote_results = generate_vote_results(session)
    insert_and_update(models.VoteResult, vote_results)


def populate_poll_results_per_fraction():
    print("Starting Process to populate poll_result_per_fraction table")
    begin_time = time.time()

    polls = session.query(Poll.id).all()
    poll_results = session.query(PollResultPerFraction.poll_id).all()
    poll_results_ids = [poll_results_id[0] for poll_results_id in poll_results]
    poll_ids = [poll_id[0] for poll_id in polls]

    poll_results_per_fraction = []
    for poll_id in poll_ids:
        if poll_id not in poll_results_ids:
            print(f"    Poll_id {poll_id} is NOT in here")
            print(f"    Creating items when poll_id is {poll_id}")
            fractions = (
                session.query(Vote.fraction_id)
                .filter(Vote.poll_id == poll_id)
                .distinct()
                .all()
            )
            fraction_ids = [fraction_id[0] for fraction_id in fractions]
            for fraction_id in fraction_ids:
                total_yes = get_total_votes_of_type(
                    "yes", poll_id, fraction_id, session
                )
                total_no = get_total_votes_of_type("no", poll_id, fraction_id, session)
                total_abstain = get_total_votes_of_type(
                    "abstain", poll_id, fraction_id, session
                )
                total_no_show = get_total_votes_of_type(
                    "no_show", poll_id, fraction_id, session
                )
                poll_result_id = int(str(poll_id) + str(fraction_id))
                poll_result = {
                    "id": poll_result_id,
                    "entity_type": "poll_result",
                    "poll_id": poll_id,
                    "fraction_id": fraction_id,
                    "total_yes": total_yes,
                    "total_no": total_no,
                    "total_abstain": total_abstain,
                    "total_no_show": total_no_show,
                }
                print(f"        -> Item of fraction_id {fraction_id} created")
                poll_results_per_fraction.append(poll_result)

    print(
        f"Inserting {len(poll_results_per_fraction)} items into poll_results_per_fraction table"
    )
    insert_and_update(models.PollResultPerFraction, poll_results_per_fraction)

    end_time = time.time()
    print(
        f"Total runtime to store {len(poll_results_per_fraction)} data is {end_time - begin_time}"
    )


def update_politicians_occupation() -> None:
    begin_time = time.time()
    session = Session()
    file_path = "src/cron_jobs/data/politicians.json"
    """has_file = has_valid_file(file_path)
     if not has_file:
        politicians_data = fetch_entity("politicians")
        write_json(file_path, politicians_data) """
    politicians = read_json(file_path)
    for politician in politicians:
        id = politician["id"]
        occupation = politician["occupation"]
        if occupation:
            session.query(Politician).filter(Politician.id == id).update(
                {Politician.occupation: occupation}
            )
            session.commit()
    end_time = time.time()
    print(f"Total runtime to update data is {end_time - begin_time}")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    insert_cv()
    # populate_cvs_and_career_paths()
