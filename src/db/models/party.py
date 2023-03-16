from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Party(Base):
    __tablename__ = "party"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String, unique=True)
    full_name = Column(String)
    short_name = Column(String)
    party_style_id = Column(Integer, ForeignKey("party_style.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "party_style": self.party_style.to_dict() if self.party_style else None,
        }

    # One to One
    party_style = relationship("PartyStyle", back_populates="party")

    # One to Many
    candidacy_mandates = relationship("CandidacyMandate", back_populates="party")
