# std
from typing import Any, Dict, List, Optional

# 3rd-party
import requests

# local
from .types import ComitteeMembership, Mandate, Politician, Poll, Sidejob, Vote


def fetch(url: str, params: Dict[str, Any] = {}):
    """Fetch from abgeordnetenwatch-API."""
    BASE_URL = "https://abgeordnetenwatch.de/api/v2"
    return requests.get(f"{BASE_URL}/{url}", params).json()["data"]


# ---


def committee_memberships(politician_name: str) -> List[ComitteeMembership]:
    return fetch(
        "committee-memberships",
        {
            "candidacy_mandate[entity.label][sw]": f"{politician_name} (Bundestag 2017 - 2021)"
        },
    )


def first_vote(constituency_id: int, parliament_period_id: int) -> List[Mandate]:
    return fetch(
        "candidacies-mandates",
        {
            "electoral_data[entity.constituency.entity.id]": constituency_id,
            "parliament_period[entity.id]": parliament_period_id,
        },
    )


def mandate(politician_id: int) -> Mandate:
    mandate_list = fetch(
        "candidacies-mandates",
        {
            "politician[entity.id]": politician_id,
            "parliament_period[entity.label][ne]": "Bundestag Wahl 2021",  # we ignore candidacies for the current election
            "type": "candidacy",  # we only take candidacies and ignore mandates
        },
    )
    # we assume that the candidacies are sorted by year, descending
    return mandate_list[0]


def image(politician_id: int) -> Optional[str]:
    IMAGE_BASE_URL = "https://candidate-images.s3.eu-central-1.amazonaws.com"
    image_url = f"{IMAGE_BASE_URL}/{politician_id}.jpg"
    if requests.head(image_url).ok:
        return image_url
    else:
        return None


def politician(id: int) -> Politician:
    return fetch(f"politicians/{id}")


def politicians_search(name: str) -> List[Politician]:
    RESULT_LIMIT = 20
    return fetch("politicians/", {"label[cn]": name, "range_end": RESULT_LIMIT})


def poll(id: int) -> Poll:
    fetch(f"polls/{id}")


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
