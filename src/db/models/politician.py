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
    party = relationship("Party")

    def to_dict(self):
        return {
            "id": self.id,
            "entity_type": self.entity_type,
            "label": self.label,
            "api_url": self.api_url,
            "abgeordnetenwatch_url": self.abgeordnetenwatch_url,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_name": self.birth_name,
            "sex": self.sex,
            "year_of_birth": self.year_of_birth,
            "party_id": self.party_id,
            "party_past": self.party_past,
            "deceased": self.deceased,
            "deceased_date": self.deceased_date,
            "education": self.education,
            "residence": self.residence,
            "occupation": self.occupation,
            "statistic_questions": self.statistic_questions,
            "statistic_questions_answered": self.statistic_questions_answered,
            "qid_wikidata": self.qid_wikidata,
            "field_title": self.field_title,
            "party": self.party.to_dict() if self.party else None,
            # Add other relationships if necessary
        }

    # One to Many
    candidacy_mandates = relationship("CandidacyMandate", back_populates="politician")
    positions = relationship("Position", back_populates="politicians")
    cvs = relationship("CV", back_populates="politician")
    weblinks = relationship("PoliticianWeblink", back_populates="politician")
