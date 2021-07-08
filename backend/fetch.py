# std
from typing import Any, Dict, List

# 3rd-party
import requests

# local
from .types import ComitteeMembership, Mandate, Politician, Sidejob, Vote


def fetch(url: str, params: Dict[str, Any] = {}):
    """Fetch from abgeordnetenwatch-API."""
    BASE_URL = "https://abgeordnetenwatch.de/api/v2"
    return requests.get(f"{BASE_URL}/{url}", params).json()["data"]


# ---


PARLIAMENT_PERIOD_ID = 50  # `parliament_period.id` of "Bundestag Wahl 2017"


def committee_memberships(politician_name: str) -> List[ComitteeMembership]:
    return fetch(
        "committee-memberships",
        {
            "candidacy_mandate[entity.label][sw]": f"{politician_name} (Bundestag 2017 - 2021)"
        },
    )


def first_vote(constituency_id: int) -> List[Mandate]:
    return fetch(
        "candidacies-mandates",
        {
            "electoral_data[entity.constituency.entity.id]": constituency_id,
            "parliament_period[entity.id]": PARLIAMENT_PERIOD_ID,
        },
    )


def mandate(politician_id: int) -> Mandate:
    mandate_list = fetch(
        "candidacies-mandates",
        {
            "politician[entity.id]": politician_id,
            "parliament_period[entity.id]": PARLIAMENT_PERIOD_ID,
        },
    )
    # list will be only one element, since there is only one mandate, per politician, per parliament_period
    return mandate_list[0]


def politician(id: int) -> Politician:
    return fetch(f"politicians/{id}")


def politicians_search(name: str) -> List[Politician]:
    RESULT_LIMIT = 20
    return fetch("politicians/", {"label[cn]": name, "range_end": RESULT_LIMIT})


def second_vote(electoral_list_id: int, party_id: int) -> List[Mandate]:
    return fetch(
        "candidacies-mandates",
        {
            "electoral_data[entity.electoral_list.entity.id]": electoral_list_id,
            "politician[entity.party.entity.id]": party_id,
        },
    )


def sidejobs(politician_name: str) -> List[Sidejob]:
    return fetch(
        "sidejobs",
        {
            "mandates[entity.label][cn]": politician_name,
        },
    )


def vote(vote_id: int, politician_name: str) -> Vote:
    return fetch(
        "votes", {"poll": vote_id, "mandate[entity.label][cn]": politician_name}
    )
