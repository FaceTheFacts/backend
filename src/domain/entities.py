from enum import Enum


class Entity(Enum):
    """
    value is the name of Abgeordnetenwatch API endpoint
    kebab-case and pluralized
    """

    PARTY = "parties"
    PARTY_STYLE = "party-styles"
    PARLIAMENT = "parliaments"
    PARLIAMENT_PERIOD = "parliament-periods"
    TOPIC = "topics"
    COMMITTEE = "committees"
    COMMITTEE_HAS_TOPIC = "committee-has-topics"
    POLL = "polls"
