# std
import re
import json
import time
from typing import List, Optional


# local
from src.cron_jobs.utils.partydonation_organisation import clean_donor
from src.cron_jobs.utils.match_topic import match_topic
from src.cron_jobs.crud_db import populate_poll_results_per_fraction
from src.cron_jobs.utils import extract_and_clean_donor
from src.cron_jobs.utils.vote_result import (
    generate_appended_vote_results,
    get_total_votes_of_type,
)
from src.cron_jobs.utils.insert_and_update import insert_and_update, insert_only
from src.cron_jobs.utils.fetch import (
    fetch_entity_data_by_ids,
    fetch_last_id_from_model,
    fetch_missing_entity,
    fetch_missing_sub_entity,
    load_entity,
    load_entity_ids_from_db,
    match_constituency_to_parliament_periods,
)
from src.db.connection import engine, Base, Session
import src.db.models as models
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


def append_candidacies(candidacies: Optional[List] = None) -> List:
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


def append_committees(committies: Optional[List] = None) -> List:
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
        sidejobs = []
        for api_sidejob in missing_sidejobs:
            income = None
            if api_sidejob["additional_information"]:
                income = extract_and_sum_amounts(api_sidejob["additional_information"])
            sidejobs.append(
                {
                    "id": api_sidejob["id"],
                    "entity_type": api_sidejob["entity_type"],
                    "label": api_sidejob["label"],
                    "api_url": api_sidejob["api_url"],
                    "job_title_extra": api_sidejob["job_title_extra"],
                    "additional_information": api_sidejob["additional_information"],
                    "category": api_sidejob["category"],
                    "income_level": api_sidejob["income_level"],
                    "income": income if income else None,
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
            )
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


def append_vote_results() -> List:
    # First Update Poll-Results-Per-Fraction
    session = Session()
    try:
        last_row = (
            session.query(models.VoteResult)
            .order_by(models.VoteResult.id.desc())
            .first()
        )
        last_id = last_row.id
        last_poll_id = last_row.poll_id
        vote_results = generate_appended_vote_results(session, last_id, last_poll_id)
        insert_and_update(models.VoteResult, vote_results)
        print("Successfully retrieved vote results")
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def append_poll_results_per_fraction():
    print("Starting Process to append poll_result_per_fraction table")
    begin_time = time.time()
    session = Session()
    try:
        # Retrieve existing poll_id and fraction_id combinations from PollResultPerFraction
        existing_poll_results = session.query(
            models.PollResultPerFraction.poll_id,
            models.PollResultPerFraction.fraction_id,
        ).all()
        existing_poll_results_ids = {
            (result.poll_id, result.fraction_id) for result in existing_poll_results
        }

        # Retrieve all poll IDs
        all_polls = session.query(models.Poll.id).all()
        new_poll_ids = {
            poll.id for poll in all_polls if poll.id not in existing_poll_results_ids
        }

        new_poll_results_per_fraction = []
        for poll_id in new_poll_ids:
            fractions = (
                session.query(models.Vote.fraction_id)
                .filter(models.Vote.poll_id == poll_id)
                .distinct()
                .all()
            )
            for fraction in fractions:
                fraction_id = fraction[0]

                # This check is now correct, as existing_poll_results_ids is properly defined
                if (poll_id, fraction_id) not in existing_poll_results_ids:
                    print(
                        f"Poll_id {poll_id} with fraction_id {fraction_id} is NOT in here. Creating entry."
                    )

                    # Calculating total votes for each type
                    total_yes = get_total_votes_of_type(
                        "yes", poll_id, fraction_id, session
                    )
                    total_no = get_total_votes_of_type(
                        "no", poll_id, fraction_id, session
                    )
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
                    new_poll_results_per_fraction.append(poll_result)

        # If there are new entries, insert them into the database
        if new_poll_results_per_fraction:
            print(
                f"Inserting {len(new_poll_results_per_fraction)} new items into poll_results_per_fraction table"
            )
            insert_and_update(
                models.PollResultPerFraction, new_poll_results_per_fraction
            )
        else:
            print("No new items to insert.")

        end_time = time.time()
        print(f"Total runtime for appending new data is {end_time - begin_time}")
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


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


def append_position_statements(file) -> List:
    match = re.search(r"-(\d+)\.json$", file)
    if match:
        parliamentPeriodId = int(match.group(1))
        print(parliamentPeriodId)
    else:
        raise ValueError("Could not extract parliamentPeriodId from filename")
    data = read_json(file)
    position_statements = []
    for item in data:
        matched_topic_id = match_topic(item["text"], item["topic"])
        entry = {
            "id": int(f"{parliamentPeriodId}{item['number']}"),
            "statement": item["text"],
            "topic_id": matched_topic_id if matched_topic_id else None,
        }
        position_statements.append(entry)
    insert_and_update(models.PositionStatement, position_statements)


def append_positions() -> List:
    # append_position_statements("assumptions-Hessen-148.json")
    filename = "positions-Hessen-148.json"
    match = re.search(r"-(\d+)\.json$", filename)
    if not match:
        raise ValueError("Could not extract parliamentPeriodId from filename")

    parliament_period = int(match.group(1))
    data = read_json(filename)
    positions = []

    for politician_id, positions_list in data.items():
        for position_data in positions_list:
            for statement_number, details in position_data.items():
                position = details.get("position", "")
                reason = details.get("reason", None)
                position_statment_id = str(parliament_period) + statement_number
                id = int(f"{parliament_period}{politician_id}{statement_number}")

                position_data_entry = {
                    "id": id,
                    "position": position,
                    "reason": reason,
                    "politician_id": int(politician_id),
                    "parliament_period_id": parliament_period,
                    "position_statement_id": int(position_statment_id),
                }
                positions.append(position_data_entry)
    insert_and_update(models.Position, positions)


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
    donations_to_append = extract_and_clean_donor.clean_donation_and_organisations(
        json_data
    )

    # Insert the cleaned donations into the database
    insert_and_update(models.PartyDonation, donations_to_append)
    print("Successfully retrieved party donations")


def append_partydonation_organization() -> None:
    api_party_donation_organizations = load_entity("partydonation")
    clean_api_party_donation_organizations = clean_donor(
        api_party_donation_organizations
    )
    party_donation_organizations = fetch_missing_entity(
        "party_donation_organizations", models.PartyDonationOrganization
    )
    insert_and_update(models.PartyDonationOrganization, party_donation_organizations)
    print("Successfully retrieved party donation organizations")


def append_cities() -> None:
    missing_cities = fetch_missing_entity("cities", models.City)
    if missing_cities:
        cities = [
            {
                "id": api_city["id"],
                "entity_type": api_city["entity_type"],
                "label": api_city["label"],
                "api_url": api_city["api_url"],
            }
            for api_city in missing_cities
        ]
        insert_and_update(models.City, cities)
        print("Successfully appended cities")
    else:
        print("No new cities to append")


def append_sidejob_organizations() -> List:
    append_countries()
    append_cities()
    missing_sidejob_organizations = fetch_missing_entity(
        "sidejob-organizations", models.SidejobOrganization
    )
    if missing_sidejob_organizations:
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
            for api_sidejob_organization in missing_sidejob_organizations
        ]
        insert_and_update(models.SidejobOrganization, sidejob_organizations)
        print("Successfully retrieved sidejob organizations")
        organization_topics = []
        for api_sidejob_organization in missing_sidejob_organizations:
            field_topics = api_sidejob_organization["field_topics"]
            if field_topics:
                for topic in field_topics:
                    organization_topic = {
                        "sidejob_organization_id": api_sidejob_organization["id"],
                        "topic_id": topic["id"],
                    }
                    organization_topics.append(organization_topic)
        if organization_topics:
            insert_only(models.SidejobOrganizationHasTopic, organization_topics)
            print("Successfully retrieved sidejob organization topics")
        return sidejob_organizations
    else:
        print("Nothing to fetch for sidejob organizations")


def append_countries() -> None:
    missing_countries = fetch_missing_entity("countries", models.Country)
    if missing_countries:
        countries = [
            {
                "id": api_country["id"],
                "entity_type": api_country["entity_type"],
                "label": api_country["label"],
                "api_url": api_country["api_url"],
            }
            for api_country in missing_countries
        ]
        insert_and_update(models.Country, countries)
        print("Successfully appended countries")
    else:
        print("No new countries to append")


def gen_images_json():
    session = Session()
    results = (
        session.query(models.Politician.id, models.Politician.abgeordnetenwatch_url)
        .order_by(models.Politician.id.desc())
        .all()
    )

    # Map the results to a list of dictionaries
    entities = [{"id": r[0], "abgeordnetenwatch_url": r[1]} for r in results]

    write_json("politicians_images.json", entities)


def extract_and_sum_amounts(s: str) -> float:
    try:
        # Regex pattern to match amounts
        pattern = r"(\d{1,3}(?:\.\d{3})*,\d{2})\s*EUR"
        matches = re.findall(pattern, s)

        # Convert each match to a float and sum them up
        total = sum(
            float(match.replace(".", "").replace(",", ".")) for match in matches
        )

        # round to two decimal places if it has decimal places
        if total % 1 == 0:
            total = round(total, 2)
            return total
        return total
    except Exception as e:
        print(e)
        return None


def update_sidejobs_income():
    # Get all sidejobs from the database sorted by id ascending:
    session = Session()
    sidejobs = session.query(models.Sidejob).order_by(models.Sidejob.id.asc()).all()
    sidejobs = [sidejob.__dict__ for sidejob in sidejobs]
    # Check if the sidejob has additional information
    sidejobs_with_additional_information = [
        sidejob for sidejob in sidejobs if sidejob["additional_information"]
    ]
    # Extract the amount from the additional information
    for sidejob in sidejobs_with_additional_information:
        amount = extract_and_sum_amounts(sidejob["additional_information"])
        # check if amount is not 0
        if amount:
            sidejob["income"] = amount
            # Update the sidejob in the database
            session.query(models.Sidejob).filter(
                models.Sidejob.id == sidejob["id"]
            ).update({"income": amount})
            session.commit()
            print(f"Updated sidejob with id {sidejob['id']} with income {amount}")
        else:
            print(f"Could not extract amount from sidejob with id {sidejob['id']}")
    print("Finished updating sidejobs")


def update_politician_images():
    with open("urls_cc.json", "r") as file:
        data = json.load(file)

    session = Session()

    for politician_id, image_data in data.items():
        copyright = image_data["copyright"]
        if copyright is None:
            continue
        # Update the politician in the database
        session.query(models.Politician).filter(
            models.Politician.id == int(politician_id)
        ).update({"image_copyright": copyright})
        session.commit()

        print(
            f"Updated politician with id {politician_id} with image source {copyright}"
        )

    print("Finished updating politician images")


def update_polls_and_votes():
    append_parliament_periods()
    append_fractions()
    append_committees()
    append_polls()
    append_politicians()
    append_candidacies()
    append_votes()
    append_poll_results_per_fraction()
    append_vote_results()


def update_sidejobs():
    append_sidejob_organizations()
    append_sidejobs()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
