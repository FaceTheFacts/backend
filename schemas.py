from pydantic import BaseModel
from pydantic.main import BaseConfig
from datetime import date
from typing import Optional, Dict
from typing_extensions import TypedDict


class Country(BaseModel):
    id: int
    label: str

    class Config:
        orm_mode = True


class Committee(BaseModel):
    id: int
    entity_type: str
    label: str

    class Config:
        orm_mode = True


class Poll(BaseModel):
    id: int
    entity_type: str
    label: str
    committee: Optional[Committee]
    field_intro: str
    field_poll_date: date

    class Config:
        orm_mode = True


class Politician(BaseModel):
    id: int
    entity_type: str
    label: str
    first_name: str
    last_name: str
    sex: Optional[str]
    year_of_birth: Optional[str]
    party_past: Optional[str]
    deceased: Optional[bool]
    deceased_date: Optional[date]
    education: Optional[str]
    residence: Optional[str]
    occupation: Optional[str]
    statistic_questions: Optional[str]
    statistic_questions_answered: Optional[str]
    qid_wikidata: Optional[str]
    field_title: Optional[str]

    class Config:
        orm_mode = True
