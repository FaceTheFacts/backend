# std
from dataclasses import dataclass
from typing import List, Dict, Any


class Event:
    pass


@dataclass
class CronJobExecuted(Event):
    job: str


# step2
@dataclass
class MissingEntityFetched(Event):
    entity: str
    data: List[Dict[str, Any]]

# step3
@dataclass
class UpdatedEntityPrepared(Event):
    entities: List[str]
    data: List[List[Dict[str, Any]]]
