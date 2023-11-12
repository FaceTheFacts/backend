# std
from dataclasses import dataclass
from typing import List, Dict, Any


class Event:
    pass


@dataclass
class CronJobExecuted(Event):
    job: str


@dataclass
class MissingEntityFetched(Event):
    entities: List[str]
    # entity: str  # maybe I should make it entity list
    # for example
    # entity = ["party", "party_style"]
    data: List[Dict[str, Any]]  # maybe I should make it data list
    # for example
    """ data = [[
        {
        "id": 1,
        "name": "Republican",
        "acronym": "REP",
        }
        # party_style
    ],[
        {
        "id": 1,
        "name": "Republican",
        "acronym": "REP",
        }
        # party
    
    ]] """


# step3
@dataclass
class UpdatedEntityPrepared(Event):
    entities: List[str]
    data: List[List[Dict[str, Any]]]
