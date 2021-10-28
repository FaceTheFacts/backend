# std
from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class Country(BaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str

    class Config:
        orm_mode = True


class City(BaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str

    class Config:
        orm_mode = True


class Topic(BaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str
    abgeordnetenwatch_url: str
    description: Optional[str]
    # parent: Optional[Topic]
    parent_id: Optional[int]

    class Config:
        orm_mode = True


# -----------------------
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


# -----------------------
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


# -----------------------
class Constituency(BaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str
    name: str
    number: Optional[int]

    class Config:
        orm_mode = True


class ElectoralDataToConstituency(BaseModel):
    id: int
    constituency: Optional[Constituency]

    class Config:
        orm_mode = True


class CandidacyMandateToConstituencies(BaseModel):
    id: int
    electoral_data: ElectoralDataToConstituency

    class Config:
        orm_mode = True


class PoliticianToConstituencies(BaseModel):
    id: int
    candidacy_mandates: List[CandidacyMandateToConstituencies]

    class Config:
        orm_mode = True


# -----------------------
class Position(BaseModel):
    id: int
    position: str
    reason: Optional[str]

    class Config:
        orm_mode = True


class PoliticianToPosition(BaseModel):
    id: int
    positions: List[Position]

    class Config:
        orm_mode = True


# -----------------------
class SidejobOrganization(BaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str
    city: Optional[City]
    country: Optional[City]
    topics: Optional[List[Topic]]

    class Config:
        orm_mode = True


# -----------------------
class Sidejob(BaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str
    job_title_extra: Optional[str]
    additional_information: Optional[str]
    category: str
    income_level: Optional[str]
    interval: Optional[str]
    data_change_date: date
    created: int
    sidejob_organization: Optional[SidejobOrganization]
    city: Optional[City]
    country: Optional[Country]
    topics: Optional[List[Topic]]

    class Config:
        orm_mode = True
