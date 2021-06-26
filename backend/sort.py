# std
from typing import List

# local
from .types import Mandate


def first_vote(first_vote: List[Mandate]) -> List[Mandate]:
    return sorted(
        first_vote,
        key=lambda x: x["electoral_data"]["constituency_result"],
        reverse=True,
    )


def second_vote(second_vote: List[Mandate]) -> List[Mandate]:
    return sorted(second_vote, key=lambda x: x["electoral_data"]["list_position"])
