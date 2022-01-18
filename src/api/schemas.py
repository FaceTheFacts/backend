# std
from pydantic import BaseModel
from datetime import date, datetime
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
    poll_passed: bool


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
class PositionStateMent(FTFBaseModel):
    statement: str


class Position(FTFBaseModel):
    id: int
    position: str
    reason: Optional[str]
    position_statement: PositionStateMent


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
    created: date
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


class PartyStyle(FTFBaseModel):
    id: int
    display_name: str
    foreground_color: str
    background_color: str
    border_color: Optional[str]


class Party(FTFBaseModel):
    id: int
    label: str
    party_style: PartyStyle


class Politician(FTFBaseModel):
    id: int
    entity_type: str
    label: str
    first_name: str
    last_name: str
    sex: Optional[str]
    year_of_birth: Optional[str]
    party: Optional[Party]
    deceased: Optional[bool]
    deceased_date: Optional[date]
    education: Optional[str]
    residence: Optional[str]
    occupations: Optional[List[str]]
    statistic_questions: Optional[str]
    statistic_questions_answered: Optional[str]
    qid_wikidata: Optional[str]
    field_title: Optional[str]
    sidejobs: Optional[List[Sidejob]]
    cvs: Optional[List]
    abgeordnetenwatch_url: Optional[str]
    weblinks: Optional[List]
    votes_and_polls: Optional[List[VoteAndPoll]]
    topic_ids_of_latest_committee: Optional[List[int]]


class PoliticianSearch(FTFBaseModel):
    id: int
    label: str
    party: Optional[Party]
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


class PoliticianSpeech(BaseModel):
    videoFileURI: Optional[str]
    title: str
    date: str


class PoliticianSpeechData(BaseModel):
    items: Optional[List[PoliticianSpeech]]
    total: int
    page: int
    size: int
    is_last_page: bool


class PolitrackImage(FTFBaseModel):
    url: str
    title: Optional[str]
    height: Optional[int]
    width: Optional[int]


class PolitrackNewsArticle(FTFBaseModel):
    id: str
    highlight: Optional[str]
    images: Optional[List[PolitrackImage]]
    published: datetime
    source: Optional[str]
    title: str
    url: str
