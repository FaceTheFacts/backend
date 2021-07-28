from typing import List
from backend.types import ComitteeMembership, Poll, Sidejob, Vote
import json


def fetch_json(path: str):
    BASE_PATH = "data/json"
    selected_path = BASE_PATH + path + ".json"
    with open(selected_path) as read_file:
        data = json.load(read_file)
    return data


def fetch_polls():
    return fetch_json("/polls_bundestag")


def fetch_politician():
    return fetch_json("/votes_bundestag_politician")


def fetch_party_votes():
    return fetch_json("/votes_bundestag")


def fetch_sidejobs():
    return fetch_json("/sidejobs")


def fetch_committee_memberships():
    return fetch_json("/committees")


def polls(id: int) -> Poll:
    polls = fetch_polls()
    selected = list(filter(lambda poll: poll["id"] == id, polls))[0]
    return selected


def politician_poll(id: int, name: str) -> Poll:
    politician_polls = fetch_politician()
    selected_by_id = list(
        filter(lambda poll: poll["poll"]["id"] == id, politician_polls)
    )
    selected_by_name = list(
        filter(lambda poll: name in poll["mandate"]["label"], selected_by_id)
    )[0]
    # Remove no_show
    if selected_by_name["vote"] == "no_show":
        return
    return selected_by_name


def party_votes(id: str) -> Vote:
    party_votes = fetch_party_votes()
    selected = party_votes[id]
    return selected


def sidejobs(politician_name: str) -> List[Sidejob]:
    sidejobsData = fetch_sidejobs()
    selected_by_name = filter(
        lambda sidejob: politician_name in sidejob["mandates"][0]["label"], sidejobsData
    )
    return list(selected_by_name)


def committee_memberships(politician_name: str) -> List[ComitteeMembership]:
    committee_membershipData = fetch_committee_memberships()
    selected_by_name = filter(
        lambda committee_membership: politician_name
        in committee_membership["candidacy_mandate"]["label"],
        committee_membershipData,
    )
    print(type(selected_by_name))
    return list(selected_by_name)


# Call all of them
def candidate_polls(id: int, name: str) -> Poll:
    politician_poll_dict = politician_poll(id, name)
    polls_dict = polls(id)
    party_votes_dict = party_votes(str(id))
    candidate_poll_dict = dict()
    candidate_poll_dict["politician-poll"] = politician_poll_dict
    candidate_poll_dict["poll-detail"] = polls_dict
    candidate_poll_dict["party-votes"] = party_votes_dict
    return candidate_poll_dict
