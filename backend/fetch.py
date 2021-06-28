# std
from typing import Any, Dict, List

# 3rd-party
import requests

# local
from .types import Mandate, Politician


def fetch(url: str, params: Dict[str, Any] = {}):
    """Fetch from abgeordnetenwatch-API."""
    BASE_URL = "https://abgeordnetenwatch.de/api/v2"
    return requests.get(f"{BASE_URL}/{url}", params).json()["data"]


# ---


PARLIAMENT_PERIOD_ID = 50  # `parliament_period.id` of "Bundestag Wahl 2017"


def first_vote(constituency_id: int) -> List[Mandate]:
    return fetch(
        "candidacies-mandates",
        params={
            "electoral_data[entity.constituency.entity.id]": constituency_id,
            "parliament_period[entity.id]": PARLIAMENT_PERIOD_ID,
        },
    )


def mandate(politician_id: int) -> Mandate:
    mandate_list = fetch(
        "candidacies-mandates",
        params={
            "politician[entity.id]": politician_id,
            "parliament_period[entity.id]": PARLIAMENT_PERIOD_ID,
        },
    )
    # list will be only one element, since there is only one mandate, per politician, per parliament_period
    return mandate_list[0]


def politician(id: int) -> Politician:
    return fetch(f"politicians/{id}")


def second_vote(electoral_list_id: int, party_id: int) -> List[Mandate]:
    return fetch(
        "candidacies-mandates",
        params={
            "electoral_data[entity.electoral_list.entity.id]": electoral_list_id,
            "politician[entity.party.entity.id]": party_id,
        },
    )
