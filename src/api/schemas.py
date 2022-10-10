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
    label: str
    party: Optional[Party]
    occupations: Optional[List[str]]
    sidejobs: Optional[List[Sidejob]]
    cvs: Optional[List]
    abgeordnetenwatch_url: Optional[str]
    weblinks: Optional[List]
    votes_and_polls: Optional[List[VoteAndPoll]]
    topic_ids_of_latest_committee: Optional[List[int]]


class PoliticianHeader(FTFBaseModel):
    id: int
    label: str
    party: Optional[Party]


class VoteResult(FTFBaseModel):
    yes: int
    no: int
    abstain: int
    no_show: int


class ConstituencyPoliticians(FTFBaseModel):
    constituency_number: int
    constituency_name: str
    politicians: List[PoliticianHeader]


class PollVotes(FTFBaseModel):
    yes: List[PoliticianHeader]
    no: List[PoliticianHeader]
    abstain: List[PoliticianHeader]
    no_show: List[PoliticianHeader]


class BundestagPollData(FTFBaseModel):
    poll: Poll
    result: VoteResult


class BundestagPollDataWithPoliticians(FTFBaseModel):
    poll: Poll
    result: VoteResult
    politicians: List[int]
    last_politician: str


class BundestagPoll(FTFBaseModel):
    data: List[BundestagPollDataWithPoliticians]
    last_page: bool


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


class PollLinks(FTFBaseModel):
    uri: str
    title: str


class PollDetails(FTFBaseModel):
    poll_results: List[PollResult]
    poll_links: List[PollLinks]


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


class ParliamentSpeech(BaseModel):
    videoFileURI: Optional[str]
    title: str
    date: str
    speaker: PoliticianHeader


class PoliticianSpeechData(BaseModel):
    items: Optional[List[PoliticianSpeech]]
    total: int
    page: int
    size: int
    is_last_page: bool
    politician_id: int


class ParliamentSpeechData(BaseModel):
    items: Optional[List[ParliamentSpeech]]
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


class SidejobBundestag(FTFBaseModel):
    sidejob: Sidejob
    politician: PoliticianHeader


class PartyDonationOrganization(FTFBaseModel):
    id: int
    donor_name: str
    donor_address: str
    donor_zip: str
    donor_city: str
    donor_foreign: bool

class PartyDonation(FTFBaseModel):
    id: int
    party: Party
    amount: float
    date: date
    party_donation_organization: PartyDonationOrganization


class HomepagePartyDonation(FTFBaseModel):
    party: Party
    donations_over_32_quarters: List[float]
    donations_total: float
    largest_donation: float
