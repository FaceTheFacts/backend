from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class PollResultPerFraction(Base):
    __tablename__ = "poll_result_per_fraction"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    poll_id = Column(Integer, ForeignKey("poll.id"))
    fraction_id = Column(Integer, ForeignKey("fraction.id"))
    total_yes = Column(Integer)
    total_no = Column(Integer)
    total_abstain = Column(Integer)
    total_no_show = Column(Integer)

    # Many to One
    poll = relationship("Poll", back_populates="poll_results_per_fraction")
    fraction = relationship("Fraction", back_populates="poll_results_per_fraction")
