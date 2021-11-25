from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base, engine


class PollResultPerParty(Base):
    __tablename__ = "poll_result_per_party"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    poll_id = Column(Integer, ForeignKey("poll.id"))
    party_id = Column(Integer, ForeignKey("party.id"))
    total_yes = Column(Integer)
    total_no = Column(Integer)
    total_abstain = Column(Integer)
    total_no_show = Column(Integer)

    # Many to One
    poll = relationship("Poll", back_populates="poll_results_per_party")
    party = relationship("Party", back_populates="poll_results_per_party")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
