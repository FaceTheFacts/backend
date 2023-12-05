# std
from dataclasses import dataclass
from typing import List


class Event:
    pass


@dataclass
class MissingEntityFetched(Event):
    entity: str
    data: List[dict]


@dataclass
class UpdatedEntityPrepared(Event):
    entities: List[str]


@dataclass
class TableUpdated(Event):
    entities: List[str]
