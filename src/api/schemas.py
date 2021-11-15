# std
from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict


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
    field_intro: str
    field_poll_date: date

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

    class Config:
        orm_mode = True


# -----------------------
class Sidejob(BaseModel):
    id: int
    entity_type: str
    label: str
    income_level: Optional[str]
    interval: Optional[str]
    data_change_date: date
    sidejob_organization: Optional[SidejobOrganization]

    class Config:
        orm_mode = True


# -----------------------
class Vote(BaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str
    mandate_id: int
    fraction_id: Optional[int]
    poll_id: int
    vote: str
    reason_no_show: Optional[str]
    reason_no_show_other: Optional[str]

    class Config:
        orm_mode = True

class VoteAndPoll(BaseModel):
    Vote: Vote
    Poll: Poll

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
    sidejobs: Optional[List[Sidejob]]
    cvs: Optional[List]
    weblinks: Optional[List]
    votes_and_polls: Optional[List[VoteAndPoll]]

    class Config:
        orm_mode = True


class PartySearch(BaseModel):
    id: int
    label: str

    class Config:
        orm_mode = True


class PoliticianSearch(BaseModel):
    id: int
    label: str
    party: Optional[PartySearch]
    image_url: Optional[str]

    class Config:
        orm_mode = True
