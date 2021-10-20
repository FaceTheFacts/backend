from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Party(Base):
    __tablename__ = "party"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String, unique=True)
    full_name = Column(String)
    short_name = Column(String)
    party_style_id = Column(Integer, ForeignKey("party_style.id"))

    # One to Many
    candidacy_mandates = relationship("CandidacyMandate", back_populates="party")
