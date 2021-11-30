# std
from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict


class FTFBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Country(FTFBaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str


class City(FTFBaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str


class Topic(FTFBaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str
    abgeordnetenwatch_url: str
    description: Optional[str]
    # parent: Optional[Topic]
    parent_id: Optional[int]


# -----------------------
class Committee(FTFBaseModel):
    id: int
    entity_type: str
    label: str


class Poll(FTFBaseModel):
    id: int
    label: Optional[str]
    field_intro: Optional[str]
    field_poll_date: date


# -----------------------
class Constituency(FTFBaseModel):
    id: int
    entity_type: str
    label: str
    api_url: str
    name: str
    number: Optional[int]


class ElectoralDataToConstituency(FTFBaseModel):
    id: int
    constituency: Optional[Constituency]


class CandidacyMandateToConstituencies(FTFBaseModel):
    id: int
    electoral_data: ElectoralDataToConstituency


class PoliticianToConstituencies(FTFBaseModel):
    id: int
    candidacy_mandates: List[CandidacyMandateToConstituencies]


# -----------------------
class Position(FTFBaseModel):
    id: int
    position: str
    reason: Optional[str]


class PoliticianToPosition(FTFBaseModel):
    id: int
    positions: List[Position]


# -----------------------
class SidejobOrganization(FTFBaseModel):
    id: int
    entity_type: str
    label: str


# -----------------------
class Sidejob(FTFBaseModel):
    id: int
    entity_type: str
    label: str
    income_level: Optional[str]
    interval: Optional[str]
    data_change_date: date
    sidejob_organization: Optional[SidejobOrganization]


# -----------------------
class Vote(FTFBaseModel):
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


class VoteAndPoll(FTFBaseModel):
    Vote: Vote
    Poll: Poll


class Politician(FTFBaseModel):
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


class PartySearch(FTFBaseModel):
    id: int
    label: str


class PoliticianSearch(FTFBaseModel):
    id: int
    label: str
    party: Optional[PartySearch]
    image_url: Optional[str]


class VoteResult(FTFBaseModel):
    yes: int
    no: int
    abstain: int
    no_show: int


class BundestagPoll(FTFBaseModel):
    poll_field_legislature_id: int
    poll_id: int
    poll_label: str
    poll_field_poll_date: date
    result: VoteResult


class Fraction(FTFBaseModel):
    id: int
    full_name: str
    short_name: str
    label: str


class PollResult(FTFBaseModel):
    id: int
    poll_id: int
    fraction: Fraction
    total_yes: int
    total_no: int
    total_abstain: int
    total_no_show: int
