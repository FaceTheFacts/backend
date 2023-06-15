# std
from typing import List, Optional


# local
from src.cron_jobs.utils.parser import gen_positions
from src.cron_jobs.crud_db import populate_poll_results_per_fraction
from src.cron_jobs.utils.vote_result import generate_appended_vote_results
from src.cron_jobs.utils.insert_and_update import insert_and_update, insert_only
from src.cron_jobs.utils.fetch import (
    fetch_entity_data_by_ids,
    fetch_last_id_from_model,
    fetch_missing_entity,
    fetch_missing_sub_entity,
    load_entity,
    load_entity_from_db,
    load_entity_ids_from_db,
    match_constituency_to_parliament_periods,
)
from src.db.connection import engine, Base, Session
import src.db.models as models
from src.api.schemas import PartyDonation
from src.cron_jobs.utils.partydonations import clean_donations
from src.cron_jobs.utils.file import read_json, write_json


def append_parliament_periods() -> List:
    missing_parliament_periods = fetch_missing_entity(
        "parliament-periods", models.ParliamentPeriod
    )
    if missing_parliament_periods:
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
                "parliament_id": api_parliament_period["parliament"]["id"],
                "previous_period_id": api_parliament_period["previous_period"]["id"],
            }
            for api_parliament_period in missing_parliament_periods
        ]
        insert_and_update(models.ParliamentPeriod, parliament_periods)
        print("Successfully retrieved candidadacies, mandates and parliament periods")


def append_constituencies() -> List:
    missing_constituencies = fetch_missing_entity("constituencies", models.Constituency)
    if missing_constituencies:
        constituencies = [
            {
                "id": api_constituency["id"],
                "entity_type": api_constituency["entity_type"],
                "label": api_constituency["label"],
                "api_url": api_constituency["api_url"],
                "name": api_constituency["name"],
                "number": api_constituency["number"],
                # Check before if the map inside match_constituency_to_parliament_periods is up-to-date
                "parliament_period_id": match_constituency_to_parliament_periods(
                    api_constituency["label"]
                ),
            }
            for api_constituency in missing_constituencies
        ]
        insert_and_update(models.Constituency, constituencies)
        print("Successfully retrieved constituencies")
    else:
        print("Nothing to fetch for constituencies")


def append_electoral_lists() -> List:
    missing_electoral_lists = fetch_missing_entity(
        "electoral-lists", models.ElectoralList
    )
    if missing_electoral_lists:
        electoral_lists = [
            {
                "id": api_electoral_list["id"],
                "entity_type": api_electoral_list["entity_type"],
                "label": api_electoral_list["label"],
                "api_url": api_electoral_list["api_url"],
                "name": api_electoral_list["name"],
                "parliament_period_id": api_electoral_list["parliament_period"]["id"],
            }
            for api_electoral_list in missing_electoral_lists
        ]
        insert_and_update(models.ElectoralList, electoral_lists)
        print("Successfully retrieved electoral lists")
    else:
        print("Nothing to fetch for electoral lists")


def append_electoral_data() -> List:
    missing_electoral_data = fetch_missing_sub_entity(
        "electoral_data", models.ElectoralData
    )
    if missing_electoral_data:
        electoral_data = [
            {
                "id": api_electoral_data["electoral_data"]["id"],
                "entity_type": api_electoral_data["electoral_data"]["entity_type"],
                "label": api_electoral_data["electoral_data"]["label"],
                "electoral_list_id": api_electoral_data["electoral_data"][
                    "electoral_list"
                ]["id"]
                if api_electoral_data["electoral_data"]["electoral_list"]
                else None,
                "list_position": api_electoral_data["electoral_data"]["list_position"]
                if api_electoral_data["electoral_data"]["list_position"]
                else None,
                "constituency_id": api_electoral_data["electoral_data"]["constituency"][
                    "id"
                ]
                if api_electoral_data["electoral_data"]["constituency"]
                else None,
                "constituency_result": api_electoral_data["electoral_data"][
                    "constituency_result"
                ]
                if api_electoral_data["electoral_data"]
                else None,
                "constituency_result_count": api_electoral_data["electoral_data"][
                    "constituency_result_count"
                ]
                if api_electoral_data["electoral_data"]
                else None,
                "mandate_won": api_electoral_data["electoral_data"]["mandate_won"]
                if api_electoral_data["electoral_data"]
                else None,
            }
            for api_electoral_data in missing_electoral_data
        ]
        insert_and_update(models.ElectoralData, electoral_data)
        print("Successfully retrieved electoral data")
    else:
        print("Nothing to fetch for electoral data")


def append_candidacies(candidacies: Optional[List]) -> List:
    append_parliament_periods()
    append_constituencies()
    append_electoral_lists()
    append_electoral_data()
    if not candidacies:
        missing_candidacies_mandates = fetch_missing_entity(
            "candidacies-mandates", models.CandidacyMandate
        )
    else:
        missing_candidacies_mandates = candidacies
    if missing_candidacies_mandates:
        candidacies_mandates = [
            {
                "id": api_candidacies_mandates["id"],
                "entity_type": api_candidacies_mandates["entity_type"],
                "label": api_candidacies_mandates["label"],
                "api_url": api_candidacies_mandates["api_url"],
                "id_external_administration": api_candidacies_mandates[
                    "id_external_administration"
                ],
                "id_external_administration_description": api_candidacies_mandates[
                    "id_external_administration_description"
                ],
                "type": api_candidacies_mandates["type"],
                "parliament_period_id": api_candidacies_mandates["parliament_period"][
                    "id"
                ],
                "politician_id": api_candidacies_mandates["politician"]["id"],
                "party_id": api_candidacies_mandates["party"]["id"]
                if "party" in api_candidacies_mandates
                else None,
                "start_date": api_candidacies_mandates["start_date"],
                "end_date": api_candidacies_mandates["end_date"],
                "info": api_candidacies_mandates["info"],
                "electoral_data_id": api_candidacies_mandates["electoral_data"]["id"],
                "fraction_membership_id": None,
            }
            for api_candidacies_mandates in missing_candidacies_mandates
        ]
        insert_and_update(models.CandidacyMandate, candidacies_mandates)


def append_committees(committies: Optional[List]) -> List:
    if not committies:
        missing_committees = fetch_missing_entity("committees", models.Committee)
    else:
        missing_committees = committies
    if missing_committees:
        committees = [
            {
                "id": api_committee["id"],
                "entity_type": api_committee["entity_type"],
                "label": api_committee["label"],
                "api_url": api_committee["api_url"],
                "field_legislature_id": api_committee["field_legislature"]["id"],
            }
            for api_committee in missing_committees
        ]
        committee_topics = []
        for api_committee in missing_committees:
            for topic in api_committee["field_topics"]:
                committee_topics.append(
                    {
                        "committee_id": api_committee["id"],
                        "topic_id": topic["id"],
                    }
                )

        insert_and_update(models.Committee, committees)
        print("Successfully retrieved committeees")
        insert_only(models.CommitteeHasTopic, committee_topics)
        print("Successfully retrieved committee topics")

    else:
        print("Nothing to fetch for committeees and committee topics")


def append_committee_memberships() -> List:
    missing_committee_memberships = fetch_missing_entity(
        "committee-memberships", models.CommitteeMembership
    )
    if missing_committee_memberships:
        committee_memberships = [
            {
                "id": api_committee_membership["id"],
                "entity_type": api_committee_membership["entity_type"],
                "label": api_committee_membership["label"],
                "api_url": api_committee_membership["api_url"],
                "committee_id": api_committee_membership["committee"]["id"],
                "candidacy_mandate_id": api_committee_membership["candidacy_mandate"][
                    "id"
                ],
                "committee_role": api_committee_membership["committee_role"],
            }
            for api_committee_membership in missing_committee_memberships
        ]
        mandate_ids = load_entity_ids_from_db(models.CandidacyMandate)
        committee_ids = load_entity_ids_from_db(models.Committee)
        missing_mandate_ids = []
        missing_committee_memberships_ids = []

        for item in committee_memberships:
            if item["candidacy_mandate_id"] not in mandate_ids:
                print("Missing mandate id: ", item["candidacy_mandate_id"])
                if item["candidacy_mandate_id"] not in missing_mandate_ids:
                    missing_mandate_ids.append(item["candidacy_mandate_id"])
            if item["committee_id"] not in committee_ids:
                print("Missing committee id: ", item["committee_id"])
                if item["committee_id"] not in missing_committee_memberships_ids:
                    missing_committee_memberships_ids.append(item["committee_id"])
        print("Missing mandate ids: ", missing_mandate_ids)
        print("Missing committee ids: ", missing_committee_memberships_ids)
        if missing_mandate_ids:
            missing_mandates = fetch_entity_data_by_ids(
                "candidacies-mandates", missing_mandate_ids
            )
            append_candidacies(missing_mandates)
        if missing_committee_memberships_ids:
            missing_commities = fetch_entity_data_by_ids(
                "committees", missing_committee_memberships_ids
            )
            append_committees(missing_commities)
        insert_and_update(models.CommitteeMembership, committee_memberships)
        print("Successfully retrieved committee memberships")
    else:
        print("Nothing to fetch for committee memberships")


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
        sidejobs_have_mandates = [
            {
                "sidejob_id": api_sidejob["id"],
                "candidacy_mandate_id": api_sidejob["mandates"][0]["id"],
            }
            for api_sidejob in missing_sidejobs
        ]
        sidejobs_have_topics = []
        for api_sidejob in missing_sidejobs:
            if api_sidejob["field_topics"]:
                for topic in api_sidejob["field_topics"]:
                    sidejobs_have_topics.append(
                        {
                            "sidejob_id": api_sidejob["id"],
                            "topic_id": topic["id"],
                        }
                    )
        insert_and_update(models.Sidejob, sidejobs)
        insert_only(models.SidejobHasMandate, sidejobs_have_mandates)
        insert_only(models.SidejobHasTopic, sidejobs_have_topics)
        print("Successfully retrieved sidejobs")
        return sidejobs
    else:
        print("Nothing to fetch for sidejobs")


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
        poll_topics = []
        poll_links = []
        last_field_related_link_id = fetch_last_id_from_model(models.FieldRelatedLink)
        for api_poll in missing_polls:
            field_topics = api_poll["field_topics"]
            if field_topics:
                for topic in field_topics:
                    poll_topic = {
                        "poll_id": api_poll["id"],
                        "topic_id": topic["id"],
                    }
                    poll_topics.append(poll_topic)
            field_links = api_poll["field_related_links"]
            if field_links:
                for link in field_links:
                    last_field_related_link_id += 1
                    poll_link = {
                        "id": last_field_related_link_id,
                        "poll_id": api_poll["id"],
                        "uri": link["uri"],
                        "title": link["title"],
                    }
                    poll_links.append(poll_link)
        insert_and_update(models.Poll, polls)
        insert_only(models.PollHasTopic, poll_topics)
        insert_only(models.FieldRelatedLink, poll_links)
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


def append_vote_results() -> List:
    # First Update Poll-Results-Per-Fraction
    session = Session()
    last_row = (
        session.query(models.VoteResult).order_by(models.VoteResult.id.desc()).first()
    )
    last_id = last_row.id
    last_poll_id = last_row.poll_id
    populate_poll_results_per_fraction()
    vote_results = generate_appended_vote_results(session, last_id, last_poll_id)
    insert_and_update(models.VoteResult, vote_results)
    print("Successfully retrieved vote results")


def append_fractions() -> List:
    missing_fractions = fetch_missing_entity("fractions", models.Fraction)
    if missing_fractions:
        fractions = [
            {
                "id": api_fraction["id"],
                "entity_type": api_fraction["entity_type"],
                "label": api_fraction["label"],
                "api_url": api_fraction["api_url"],
                "full_name": api_fraction["full_name"],
                "short_name": api_fraction["short_name"],
                "legislature_id": api_fraction["legislature"]["id"],
            }
            for api_fraction in missing_fractions
        ]
        insert_and_update(models.Fraction, fractions)
        print("Successfully retrieved fractions")
        return fractions


def append_positions() -> List:
    # Lookup positions related parliament_period and add it to PERIOD_POSITIONS_TABLE inside parser.py
    # Generate positions.json inside Scrapy repo src/politicians-positions/berlin.ts
    parliamend_period_id = 136
    missing_positions = gen_positions(parliamend_period_id)
    if missing_positions:
        insert_and_update(models.Position, missing_positions)


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


def append_zip_codes() -> List:
    new_entries = []
    data_base = []
    constituency_number_zip_codes_map = read_json(
        "src/cron_jobs/data/zip_codes_complete.json"
    )
    session = Session()
    constituency_table = (
        session.query(models.Constituency)
        .where(models.Constituency.parliament_period_id == 128)
        .order_by(models.Constituency.number.asc())
        .all()
    )
    for item in constituency_number_zip_codes_map:
        new_entry = [item["id"][:3], item["id"][6:]]
        new_entries.append(new_entry)
    last_id = fetch_last_id_from_model(models.ZipCode)
    for entry in new_entries:
        for item in constituency_table:
            item_number = str(item.number)
            if entry[0][0] == "0":
                if item_number == entry[0][1:]:
                    last_id += 1
                    new_entry = {
                        "id": last_id,
                        "constituency_id": item.id,
                        "zip_code": entry[1],
                    }
                    data_base.append(new_entry)
            else:
                if item_number == entry[0]:
                    last_id += 1
                    new_entry = {
                        "id": last_id,
                        "zip_code": entry[1],
                        "constituency_id": item.id,
                    }
                    data_base.append(new_entry)
    insert_and_update(models.ZipCode, data_base)


def append_partydonation(json_data: str) -> None:
    party_donations = read_json(json_data)

    parties = load_entity_from_db(models.Party)
    donor_orgs = load_entity_from_db(models.PartyDonationOrganization)
    clean_donation = clean_donations(party_donations, parties, donor_orgs)

    donations_to_append = []
    for donation in clean_donation:
        donation_to_append = {
            "id": donation["id"],
            "party_id": donation["party_id"],
            "amount": donation["amount"],
            "date": donation["date"],
            "party_donation_organization_id": donation[
                "party_donation_organization_id"
            ],
        }

        donations_to_append.append(donation_to_append)

    # Insert the cleaned donations into the database
    insert_and_update(PartyDonation, donations_to_append)
    print("Successfully retrieved party donations")


def append_partydonation_organization() -> None:
    party_donation_organizations = fetch_missing_entity(
        "party_donation_organizations", models.PartyDonationOrganization
    )
    insert_and_update(models.PartyDonationOrganization, party_donation_organizations)
    print("Successfully retrieved party donation organizations")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
