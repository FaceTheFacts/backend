from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship

from src.db.connection import Base


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
    party_id = Column(Integer, ForeignKey("party.id"))
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
    image_copyright = Column(String)
    party = relationship("Party")

    # One to Many
    candidacy_mandates = relationship("CandidacyMandate", back_populates="politician")
    positions = relationship("Position", back_populates="politicians")
    cvs = relationship("CV", back_populates="politician")
    weblinks = relationship("PoliticianWeblink", back_populates="politician")
