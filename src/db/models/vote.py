from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Vote(Base):
    __tablename__ = "vote"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    mandate_id = Column(Integer, ForeignKey("candidacy_mandate.id"))
    fraction_id = Column(Integer, ForeignKey("fraction.id"))
    poll_id = Column(Integer, ForeignKey("poll.id"))
    vote = Column(String)
    reason_no_show = Column(String)
    reason_no_show_other = Column(String)

    # Many to One
    candidacy_mandate = relationship("CandidacyMandate", back_populates="votes")
    fraction = relationship("Fraction", back_populates="votes")
    poll = relationship("Poll", back_populates="votes")
