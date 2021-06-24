# std
from typing import List

# local
from .types import Mandate


def second_vote(second_vote: List[Mandate]) -> List[Mandate]:
    return sorted(second_vote, key=lambda x: x["electoral_data"]["list_position"])
