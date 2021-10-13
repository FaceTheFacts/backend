from sqlalchemy import Column, String, Integer, ForeignKey, Text, Date, Boolean, Float
from sqlalchemy.orm import relationship

from database import Base


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String, unique=True)


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


class Committee(Base):
    __tablename__ = "committee"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    # One to Many
    polls = relationship("Poll", back_populates="committee")


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
    # sidejobs = relationship(
    #     "Sidejob",
    #     secondary="sidejob_has_mandate",
    #     back_populates="candidacy_mandates",
    # )

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