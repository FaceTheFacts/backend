# std
from dataclasses import dataclass
from typing import Any, List


class Command:
    pass


@dataclass
class FetchMissingEntity(Command):
    entity: str
    session: Any


@dataclass
class PrepareUpdateData(Command):
    entity: str
    data: List[Any]


@dataclass
class UpdateTable(Command):
    entities: List[str]
    data: List[Any]
    session: Any
