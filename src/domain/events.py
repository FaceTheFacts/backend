# std
from dataclasses import dataclass
from typing import List, Any


class Event:
    pass


@dataclass
class MissingEntityFetched(Event):
    entity: str
    data: List[Any]


@dataclass
class UpdatedEntityPrepared(Event):
    entities: List[str]
    data: List[Any]
