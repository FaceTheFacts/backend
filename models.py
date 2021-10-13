from sqlalchemy import Column, String, Integer, ForeignKey, Text, Date, Boolean, Float
from sqlalchemy.orm import relationship

from database import Base


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String, unique=True)
    # One to Many
    sidejob_organizations = relationship(
        "SidejobOrganization", back_populates="country"
    )
    # One to Many
    sidejobs = relationship("Sidejob", back_populates="country")


class City(Base):
    __tablename__ = "city"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String, unique=True)
    # One to Many
    sidejob_organizations = relationship("SidejobOrganization", back_populates="city")
    # One to Many
    sidejobs = relationship("Sidejob", back_populates="city")


class Topic(Base):
    __tablename__ = "topic"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    abgeordnetenwatch_url = Column(String)
    description = Column(String)
    parent_id = Column(Integer(), ForeignKey("topic.id"))
    committees = relationship(
        "Committee", secondary="committee_has_topic", back_populates="topics"
    )
    # Many to Many
    polls = relationship("Poll", secondary="poll_has_topic", back_populates="topics")
    sidejob_organizations = relationship(
        "SidejobOrganization",
        secondary="sidejob_organization_has_topic",
        back_populates="topics",
    )
    # Many to Many
    sidejobs = relationship(
        "Sidejob",
        secondary="sidejob_has_topic",
        back_populates="topics",
    )
    # position_statements = relationship("Position_statement", back_populates="topics")


class Poll(Base):
    __tablename__ = "poll"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    field_committees_id = Column(Integer, ForeignKey("committee.id"))
    field_intro = Column(Text)
    field_poll_date = Column(Date)
    # Many to One
    committee = relationship("Committee", back_populates="polls")
    # parliament_period = relationship("Parliament_period", back_populates="polls")
    # Many to Many
    topics = relationship("Topic", secondary="poll_has_topic", back_populates="polls")
    # One to Many
    # field_related_links = relationship("FieldRelatedLink", back_populates="poll")
    # votes = relationship("Vote", back_populates="poll")


class PollHasTopic(Base):
    __tablename__ = "poll_has_topic"
    poll_id = Column(Integer, ForeignKey("poll.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), primary_key=True)


class Committee(Base):
    __tablename__ = "committee"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    #Many to Many
    topics = relationship(
        "Topic", secondary="committee_has_topic", back_populates="committees"
    )
    # One to Many
    # committee_memberships = relationship(
    #     "Committee_membership", back_populates="committee"
    # )
    polls = relationship("Poll", back_populates="committee")

class Committee_has_topic(Base):
    __tablename__ = "committee_has_topic"
    committee_id = Column(Integer(), ForeignKey("committee.id"), primary_key=True)
    topic_id = Column(Integer(), ForeignKey("topic.id"), primary_key=True)


class Politician(Base):
    __tablename__ = "politician"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    abgeordnetenwatch_url = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birth_name = Column(String)
    sex = Column(String)
    year_of_birth = Column(String)
    # party_id = Column(Integer, ForeignKey("party.id"))
    party_past = Column(String)
    deceased = Column(Boolean)
    deceased_date = Column(Date)
    education = Column(String)
    residence = Column(String)
    occupation = Column(String)
    statistic_questions = Column(String)
    statistic_questions_answered = Column(String)
    qid_wikidata = Column(String)
    field_title = Column(String)

    # # Many to One
    # party = relationship("Party")

    # # One to Many
    candidacy_mandates = relationship("Candidacy_mandate", back_populates="politician")
    # positions = relationship("Position", back_populates="politician")


class Candidacy_mandate(Base):
    __tablename__ = "candidacy_mandate"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    id_external_administration = Column(String)
    id_external_administration_description = Column(String)
    type = Column(String)
    # parliament_period_id = Column(Integer, ForeignKey("parliament_period.id"))
    politician_id = Column(Integer, ForeignKey("politician.id"))
    # party_id = Column(Integer, ForeignKey("party.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    info = Column(String)
    electoral_data_id = Column(Integer, ForeignKey("electoral_data.id"))
    # fraction_membership_id = Column(Integer, ForeignKey("fraction_membership.id"))

    # # Many to One
    # parliament_period = relationship(
    #     "Parliament_period", back_populates="candidacy_mandates"
    # )
    politician = relationship("Politician", back_populates="candidacy_mandates")
    # party = relationship("Party", back_populates="candidacy_mandates")
    # # One to One
    electoral_data = relationship(
        "Electoral_data", back_populates="candidacy_mandate", uselist=False
    )
    # fraction_membership = relationship(
    #     "Fraction_membership", back_populates="candidacy_mandate", uselist=False
    # )
    # # One to Many
    # committee_memberships = relationship(
    #     "Committee_membership", back_populates="candidacy_mandate"
    # )
    # votes = relationship("Vote", back_populates="candidacy_mandate")
    # # Many to Many
    sidejobs = relationship(
        "Sidejob",
        secondary="sidejob_has_mandate",
        back_populates="candidacy_mandates",
    )


class Electoral_data(Base):
    __tablename__ = "electoral_data"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    # electoral_list_id = Column(Integer, ForeignKey("electoral_list.id"))
    list_position = Column(Integer)
    constituency_id = Column(Integer, ForeignKey("constituency.id"))
    constituency_result = Column(Float)
    constituency_result_count = Column(Integer)
    mandate_won = Column(String)
    # electoral_list = relationship("Electoral_list", back_populates="electoral_data")
    constituency = relationship("Constituency", back_populates="electoral_data")
    # One to One
    candidacy_mandate = relationship(
        "Candidacy_mandate", back_populates="electoral_data"
    )


class Constituency(Base):
    __tablename__ = "constituency"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    name = Column(String)
    number = Column(Integer)
    # parliament_period_id = Column(Integer, ForeignKey("parliament_period.id"))
    # parliament_period = relationship("Parliament_period")
    electoral_data = relationship("Electoral_data", back_populates="constituency")


class Sidejob(Base):
    __tablename__ = "sidejob"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    job_title_extra = Column(String)
    additional_information = Column(String)
    category = Column(String)
    income_level = Column(String)
    interval = Column(String)
    data_change_date = Column(Date)
    created = Column(Integer)
    sidejob_organization_id = Column(Integer, ForeignKey("sidejob_organization.id"))
    field_city_id = Column(Integer, ForeignKey("city.id"))
    field_country_id = Column(Integer, ForeignKey("country.id"))
    # Many to One
    sidejob_organization = relationship(
        "SidejobOrganization", back_populates="sidejobs"
    )
    city = relationship("City", back_populates="sidejobs")
    country = relationship("Country", back_populates="sidejobs")
    # Many to Many
    candidacy_mandates = relationship(
        "Candidacy_mandate",
        secondary="sidejob_has_mandate",
        back_populates="sidejobs",
    )
    topics = relationship(
        "Topic",
        secondary="sidejob_has_topic",
        back_populates="sidejobs",
    )


class SidejobHasMandate(Base):
    __tablename__ = "sidejob_has_mandate"
    sidejob_id = Column(Integer, ForeignKey("sidejob.id"), primary_key=True)
    candidacy_mandate_id = Column(
        Integer, ForeignKey("candidacy_mandate.id"), primary_key=True
    )


class SidejobHasTopic(Base):
    __tablename__ = "sidejob_has_topic"
    sidejob_id = Column(Integer, ForeignKey("sidejob.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), primary_key=True)


class SidejobOrganization(Base):
    __tablename__ = "sidejob_organization"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    field_city_id = Column(Integer, ForeignKey("city.id"))
    field_country_id = Column(Integer, ForeignKey("country.id"))
    # Many to One
    city = relationship("City", back_populates="sidejob_organizations")
    country = relationship("Country", back_populates="sidejob_organizations")
    # One to Many
    sidejobs = relationship("Sidejob", back_populates="sidejob_organization")
    # Many to Many
    topics = relationship(
        "Topic",
        secondary="sidejob_organization_has_topic",
        back_populates="sidejob_organizations",
    )


class SidejobOrganizationHasTopic(Base):
    __tablename__ = "sidejob_organization_has_topic"
    sidejob_organization_id = Column(
        Integer, ForeignKey("sidejob_organization.id"), primary_key=True
    )
    topic_id = Column(Integer, ForeignKey("topic.id"), primary_key=True)
