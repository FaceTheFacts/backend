# std
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List, Dict


class FTFBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Country(FTFBaseModel):
    id: int = Field(..., description="The unique ID of the country")
    entity_type: str = Field(
        ..., description="The type of the entity representing the country"
    )
    label: str = Field(..., description="The name of the country")
    api_url: str = Field(..., description="The API URL for retrieving country data")

    class Config:
        schema_extra = {
            "example": {
                "id": 61,
                "entity_type": "taxonomy_term",
                "label": "Deutschland",
                "api_url": "https://www.abgeordnetenwatch.de/api/v2/countries/61",
            }
        }


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
    number: int


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
class PositionStatement(FTFBaseModel):
    statement: str


class Position(FTFBaseModel):
    id: int
    position: str
    reason: Optional[str]
    position_statement: PositionStatement


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
    id: int = Field(..., description="The unique ID of the party style")
    display_name: str = Field(..., description="The display name of the party")
    foreground_color: str = Field(
        ..., description="The foreground color for the party logo"
    )
    background_color: str = Field(
        ..., description="The background color for the party logo"
    )
    border_color: Optional[str] = Field(
        None, description="The border color for the party logo, if applicable"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "display_name": "CDU",
                "foreground_color": "#FFFFFF",
                "background_color": "#636363",
                "border_color": None,
            }
        }


class Party(FTFBaseModel):
    id: int = Field(..., description="The unique ID of the party")
    label: str = Field(..., description="The full name of the political party")
    party_style: PartyStyle = Field(
        ..., description="The style information associated with the party"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "label": "CDU",
                "party_style": {
                    "id": 2,
                    "display_name": "CDU",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#636363",
                    "border_color": None,
                },
            }
        }


class Politician(FTFBaseModel):
    id: int = Field(..., description="The unique ID of the politician")
    label: str = Field(..., description="The full name of the politician")
    party: Party = Field(..., description="The party the politician belongs to")
    occupations: Optional[List[str]] = Field(
        None, description="A list of occupations held by the politician"
    )
    sidejobs: Optional[List[Sidejob]] = Field(
        None, description="A list of side jobs held by the politician"
    )
    cvs: Optional[List] = Field(
        None, description="A list of curriculum vitae entries for the politician"
    )
    abgeordnetenwatch_url: str = Field(
        None, description="The URL of the politician's profile on abgeordnetenwatch.de"
    )
    weblinks: Optional[List] = Field(
        None, description="A list of external web links related to the politician"
    )
    votes_and_polls: Optional[List[VoteAndPoll]] = Field(
        None, description="A list of votes and polls the politician participated in"
    )
    topic_ids_of_latest_committee: Optional[List[int]] = Field(
        None,
        description="A list of topic IDs related to the latest committee the politician is involved in",
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 79137,
                "label": "Angela Merkel",
                "party": {
                    "id": 2,
                    "label": "CDU",
                    "party_style": {
                        "id": 2,
                        "display_name": "CDU",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#636363",
                        "border_color": None,
                    },
                },
                "occupations": ["Bundeskanzlerin a.D."],
                "sidejobs": [
                    {
                        "id": 1523,
                        "entity_type": "sidejob",
                        "label": "Mitglied des Ehrensenats",
                        "income_level": None,
                        "interval": None,
                        "created": "2017-05-24",
                        "sidejob_organization": {
                            "id": 1456,
                            "entity_type": "sidejob_organization",
                            "label": "Stiftung Lindauer Nobelpreisträgertreffen am Bodensee",
                        },
                    },
                    {
                        "id": 1522,
                        "entity_type": "sidejob",
                        "label": "Mitglied des Kuratoriums",
                        "income_level": None,
                        "interval": None,
                        "created": "2017-05-24",
                        "sidejob_organization": {
                            "id": 1455,
                            "entity_type": "sidejob_organization",
                            "label": "Stiftung Frauenkirche Dresden",
                        },
                    },
                    {
                        "id": 1520,
                        "entity_type": "sidejob",
                        "label": "Ehrenmitglied des Kuratoriums",
                        "income_level": None,
                        "interval": None,
                        "created": "2017-05-24",
                        "sidejob_organization": {
                            "id": 732,
                            "entity_type": "sidejob_organization",
                            "label": "Stiftung Deutsche Sporthilfe (DSH)",
                        },
                    },
                    {
                        "id": 1519,
                        "entity_type": "sidejob",
                        "label": "Mitglied des Vorstandes",
                        "income_level": None,
                        "interval": None,
                        "created": "2017-05-24",
                        "sidejob_organization": {
                            "id": 249,
                            "entity_type": "sidejob_organization",
                            "label": "Konrad-Adenauer-Stiftung e.V.",
                        },
                    },
                    {
                        "id": 1518,
                        "entity_type": "sidejob",
                        "label": "Ehrenpräsidentin des Kuratoriums",
                        "income_level": None,
                        "interval": None,
                        "created": "2017-05-24",
                        "sidejob_organization": {
                            "id": 1044,
                            "entity_type": "sidejob_organization",
                            "label": "Deutsches Museum",
                        },
                    },
                    {
                        "id": 1517,
                        "entity_type": "sidejob",
                        "label": "Mitglied des Kuratoriums",
                        "income_level": None,
                        "interval": None,
                        "created": "2017-05-24",
                        "sidejob_organization": {
                            "id": 1453,
                            "entity_type": "sidejob_organization",
                            "label": "Deutsche Gesellschaft e.V., Verein zur Förderung politischer, kultureller und sozialer Beziehungen in Europa",
                        },
                    },
                    {
                        "id": 1515,
                        "entity_type": "sidejob",
                        "label": "Vorsitzende des Kuratoriums",
                        "income_level": None,
                        "interval": None,
                        "created": "2017-05-24",
                        "sidejob_organization": {
                            "id": 1022,
                            "entity_type": "sidejob_organization",
                            "label": "Bundesakademie für Sicherheitspolitik (BAKS)",
                        },
                    },
                ],
                "cvs": [
                    {
                        "id": 132,
                        "short_description": "Geboren am 17. Juli 1954 in Hamburg; evangelisch; verheiratet.",
                        "politician_id": 79137,
                        "raw_text": "Abitur 1973 in Templin. Physikstudium an der Universität Leipzig 1973 bis 1978. Wissenschaftliche Mitarbeiterin am Zentralinstitut für Physikalische Chemie an der Akademie der Wissenschaften 1978 bis 1990; Promotion 1986. Stellvertretende Regierungssprecherin der Regierung de Maizière 1990; Referentin im Presse- und Informationsamt der Bundesregierung 1990. 1989 Mitglied des „Demokratischen Aufbruchs“, seit 1990 Mitglied der CDU; Juni 1993 bis April 2000 Vorsitzende der CDU Mecklenburg-Vorpommern; Dezember 1991 bis November 1998 stellvertretende Vorsitzende der CDU Deutschlands; 7. November 1998 bis 10. April 2000 Generalsekretärin und von April 2000 bis 2018 Vorsitzende der CDU Deutschlands. Mitglied des Bundestages seit 1990; 18. Januar 1991 bis 17. November 1994 Bundesministerin für Frauen und Jugend; 17. November 1994 bis 26. Oktober 1998 Bundesministerin für Umwelt, Naturschutz und Reaktorsicherheit. September 2002 bis November 2005 Vorsitzende der CDU/CSU-Fraktion; seit 22. November 2005 Bundeskanzlerin der Bundesrepublik Deutschland. ",
                    }
                ],
                "abgeordnetenwatch_url": "https://www.abgeordnetenwatch.de/profile/angela-merkel",
                "weblinks": [
                    {
                        "politician_id": 79137,
                        "link": "http://www.bundestag.de/abgeordnete/biografien/M/merkel_angela/521968",
                        "id": 43985,
                    },
                    {
                        "politician_id": 79137,
                        "link": "https://instagram.com/bundeskanzlerin/",
                        "id": 43986,
                    },
                    {
                        "politician_id": 79137,
                        "link": "https://www.angela-merkel.de/",
                        "id": 43987,
                    },
                    {
                        "politician_id": 79137,
                        "link": "https://de.wikipedia.org/wiki/Angela_Merkel",
                        "id": 43988,
                    },
                    {
                        "politician_id": 79137,
                        "link": "https://www.facebook.com/AngelaMerkel",
                        "id": 43989,
                    },
                ],
                "votes_and_polls": [
                    {
                        "Vote": {
                            "id": 418919,
                            "entity_type": "vote",
                            "label": "Angela Merkel - Einsatz deutscher Streitkräfte zur militärischen Evakuierung aus Afghanistan",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/418919",
                            "mandate_id": 44550,
                            "fraction_id": 81,
                            "poll_id": 4283,
                            "vote": "yes",
                            "reason_no_show": None,
                            "reason_no_show_other": None,
                        },
                        "Poll": {
                            "id": 4283,
                            "label": "Einsatz deutscher Streitkräfte zur militärischen Evakuierung aus Afghanistan",
                            "field_intro": '<p>Der von der Bundesregierung eingebrachte <a class="link-download" href="https://dserver.bundestag.de/btd/19/320/1932022.pdf">Antrag</a> sieht vor, dass der Bundestag rückwirkend der Entsendung von deutschen Streitkräften nach Afghanistan zustimmt. Diese Entscheidung wurde bereits am 15. August durch den Krisenstab der Bundesregierung getroffen. Angesichts der sich dramatisch verschlechterten Sicherheitslage in Afghanistan soll die militärische Evakuierung fortgesetzt werden.</p>\r\n\r\n<p>Der Antrag wurde mit 538 Ja-Stimmen aus den Reihen aller Fraktionen <strong>angenommen</strong>. Neun Abgeordnete, insbesondere aus der Fraktion Die LINKE, stimmten gegen den Antrag. Dabei enthielten sich 89 Abgeordnete der AfD- und Die LINKE-Fraktion.</p>\r\n',
                            "field_poll_date": "2021-08-25",
                            "poll_passed": True,
                        },
                    },
                    {
                        "Vote": {
                            "id": 402063,
                            "entity_type": "vote",
                            "label": "Angela Merkel - Verbesserung des Schutzes von Gerichtsvollziehern vor Gewalt sowie zur Änderung weiterer zwangsvollstreckungsrechtlicher Vorschriften",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/402063",
                            "mandate_id": 44550,
                            "fraction_id": 81,
                            "poll_id": 4124,
                            "vote": "yes",
                            "reason_no_show": None,
                            "reason_no_show_other": None,
                        },
                        "Poll": {
                            "id": 4124,
                            "label": "Verbesserung des Schutzes von Gerichtsvollziehern vor Gewalt sowie zur Änderung weiterer zwangsvollstreckungsrechtlicher Vorschriften",
                            "field_intro": '<p>Der <a href="https://dip21.bundestag.de/dip21/btd/19/276/1927636.pdf">Gesetzesentwurf</a> der Bundesregierung sieht eine Änderung im Handlungsspielraum von Gerichtsvollziehern vor, denen es von nun an erlaubt sein soll, vor dem Besuch eines Schuldners Informationen über diesen bei der Polizei einzuholen. Auch werden die Bedingungen für die Vollstreckung eines Gerichtsvollzugs angepasst.</p>\r\n\r\n<p>&nbsp;</p>\r\n',
                            "field_poll_date": "2021-05-06",
                            "poll_passed": True,
                        },
                    },
                    {
                        "Vote": {
                            "id": 397513,
                            "entity_type": "vote",
                            "label": "Angela Merkel - Nachtragshaushalt 2021",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/397513",
                            "mandate_id": 44550,
                            "fraction_id": 81,
                            "poll_id": 4099,
                            "vote": "yes",
                            "reason_no_show": None,
                            "reason_no_show_other": None,
                        },
                        "Poll": {
                            "id": 4099,
                            "label": "Nachtragshaushalt 2021",
                            "field_intro": '<p>In Ihrem <strong><a href="https://dip21.bundestag.de/dip21/btd/19/278/1927800.pdf">Gesetzesentwurf</a></strong> hat die Bundesregierung einen ergänzenden Nachtrag errechnet, der zum Jahr 2021 hinzugefügt werden soll, zu dem auch der Bundesrat eine <a href="https://dip21.bundestag.de/dip21/btd/19/281/1928139.pdf"><strong>Stellungnahme</strong></a> vorlegte. Zusätzlich legten die Fraktionen CDU/CSU und SPD einen Antrag vor, mit dem der benötigte&nbsp;Beschluss wegen Überschreitung der grundgesetzlich festgeschriebenen Kreditobergrenzen erwirkt werden soll. Der Haushaltsausschuss legte zu beiden Anliegen eine Beschlussempfehlung vor.</p>\r\n\r\n<p>Die Fraktionen CDU/CSU und SPD stimmten geschlossen für den Gesetzesentwurf, während die Fraktion AfD geschlossen mit Nein stimmte. Die Fraktionen FDP, DIE LINKE und DIE GRÜNEN enthielten sich. <a class="link-profile" href="https://www.abgeordnetenwatch.de/profile/alexander-kulitz">Alexander Kulitz</a>, Mitglied der Fraktion FDP, stimmte ebenfalls dagegen.</p>\r\n',
                            "field_poll_date": "2021-04-23",
                            "poll_passed": True,
                        },
                    },
                    {
                        "Vote": {
                            "id": 395384,
                            "entity_type": "vote",
                            "label": "Angela Merkel - Änderung des Infektionsschutzgesetzes",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/395384",
                            "mandate_id": 44550,
                            "fraction_id": 81,
                            "poll_id": 4098,
                            "vote": "yes",
                            "reason_no_show": None,
                            "reason_no_show_other": None,
                        },
                        "Poll": {
                            "id": 4098,
                            "label": "Änderung des Infektionsschutzgesetzes",
                            "field_intro": '<p>Mit einer Änderung des Infektionsschutzgesetzes soll in Bezug auf die COVID-19-Pandemie&nbsp;eine "bundesweite Notbremse" umgesetzt werden. Der <a class="link-read-more" href="https://dip21.bundestag.de/dip21/btd/19/284/1928444.pdf">Gesetzentwurf </a>der Regierungsfraktionen CDU/CSU und SPD soll dafür sorgen, dass ab einer Inzidenz von 100 zukünftig bundeseinheitliche Regelungen greifen. Zu diesen einheitlichen Regelungen zählen unter anderem Ausgangsbeschränkungen, das Schließen von Freizeiteinrichtungen und Gaststätten, das Aussetzen des Präsenzunterrichts ab einer Inzidenz von über 165 sowie erweiterte Möglichkeiten für das Arbeiten im Homeoffice.</p>\r\n\r\n<p>Namentlich abgestimmt wird über eine <a class="link-read-more" href="https://dip21.bundestag.de/dip21/btd/19/286/1928692.pdf">Beschlussempfehlung </a>des Ausschusses für Gesundheit, der die Annahme des Gesetzentwurfs von CDU/CSU und SPD empfiehlt.</p>\r\n\r\n<p>Mit 342 Zustimmungen wurde der Gesetzentwurf der Bundesregierung angenommen, dagegen stimmten 250 Abgeordnete, 64 Abgeordnete enthielten sich.</p>\r\n',
                            "field_poll_date": "2021-04-21",
                            "poll_passed": False,
                        },
                    },
                    {
                        "Vote": {
                            "id": 375287,
                            "entity_type": "vote",
                            "label": "Angela Merkel - Erneuerbare-Energien-Gesetz (EEG)",
                            "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/375287",
                            "mandate_id": 44550,
                            "fraction_id": 81,
                            "poll_id": 3972,
                            "vote": "yes",
                            "reason_no_show": None,
                            "reason_no_show_other": None,
                        },
                        "Poll": {
                            "id": 3972,
                            "label": "Erneuerbare-Energien-Gesetz (EEG)",
                            "field_intro": '<p>Der <a href="https://dip21.bundestag.de/dip21/btd/19/234/1923482.pdf">Gesetzesentwurf</a> der Bundesregierung beinhaltet einige Änderungen am Erneuerbare-Energien-Gesetz (EEG) und bezieht sich vor allem auf die Vorgehensweise mit alten Photovoltaikanlagen sowie einigen anderen Gesichtspunkten, die die CO2 Emissionen bis 2050 auf 0 reduzieren sollen.</p>\r\n\r\n<p>Die Fraktionen der SPD und der CDU/CSU stimmten fast ausnahmslos <strong>fü</strong>r die Gesetzesänderungen während die Fraktionen der FDP, DIE GRÜNEN, DIE LINKE und AfD <strong>gegen</strong> die Änderungen am EEG stimmten. <a class="link-profile" href="https://www.abgeordnetenwatch.de/profile/arnold-vaatz">Arnold Vaatz</a> stimmte als einziges Mitglied der CDU ebenfalls <strong>gegen</strong> die Gesetzesänderungen und <a class="link-profile" href="https://www.abgeordnetenwatch.de/profile/christoph-hoffmann">Christoph Hoffmann</a>, Mitglied der Fraktion FDP, enthielt sich.</p>\r\n',
                            "field_poll_date": "2020-12-17",
                            "poll_passed": True,
                        },
                    },
                ],
                "topic_ids_of_latest_committee": [],
            },
        }


class PoliticianHeader(FTFBaseModel):
    id: int = Field(..., description="The unique ID of the politician")
    label: str = Field(..., description="The name of the politician")
    party: Party = Field(
        ..., description="The political party the politician belongs to"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 79137,
                "label": "Angela Merkel",
                "party": {
                    "id": 2,
                    "label": "CDU",
                    "party_style": {
                        "id": 2,
                        "display_name": "CDU",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#636363",
                        "border_color": None,
                    },
                },
            }
        }


class VoteResult(FTFBaseModel):
    yes: int
    no: int
    abstain: int
    no_show: int


class ConstituencyPoliticians(FTFBaseModel):
    constituency_number: int = Field(..., description="The number of the constituency")
    constituency_name: str = Field(..., description="The name of the constituency")
    politicians: List[PoliticianHeader] = Field(
        ..., description="A list of politicians representing the constituency"
    )

    class Config:
        schema_extra = {
            "example": {
                "constituency_number": 15,
                "constituency_name": "Vorpommern-Rügen - Vorpommern-Greifswald I",
                "politicians": [
                    {
                        "id": 79137,
                        "label": "Angela Merkel",
                        "party": {
                            "id": 2,
                            "label": "CDU",
                            "party_style": {
                                "id": 2,
                                "display_name": "CDU",
                                "foreground_color": "#FFFFFF",
                                "background_color": "#636363",
                                "border_color": None,
                            },
                        },
                    }
                ],
            }
        }


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
    largest_quarter: float
