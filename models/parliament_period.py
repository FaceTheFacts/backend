from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship


from ..db.base import Base


class ParliamentPeriod(Base):
    __tablename__ = "parliament_period"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    abgeordnetenwatch_url = Column(String)
    type = Column(String)
    election_date = Column(Date)
    start_date_period = Column(Date)
    end_date_period = Column(Date)
    parliament_id = Column(Integer, ForeignKey("parliament.id"))
    previous_period_id = Column(Integer, ForeignKey("parliament_period.id"))
    parliament = relationship("Parliament")

    # One to Many
    candidacy_mandates = relationship(
        "CandidacyMandate", back_populates="parliament_period"
    )
    polls = relationship("Poll", back_populates="parliament_period")
    positions = relationship("Position", back_populates="parliament_periods")
