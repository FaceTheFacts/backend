from sqlalchemy import Column, String, Integer, ForeignKey, Date, Text
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Poll(Base):
    __tablename__ = "poll"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    field_committees_id = Column(Integer, ForeignKey("committee.id"))
    field_intro = Column(Text)
    field_legislature_id = Column(Integer, ForeignKey("parliament_period.id"))
    field_poll_date = Column(Date)

    # Many to One
    committee = relationship("Committee", back_populates="polls")
    parliament_period = relationship("ParliamentPeriod", back_populates="polls")

    # Many to Many
    topics = relationship("Topic", secondary="poll_has_topic", back_populates="polls")

    # One to Many
    field_related_links = relationship("FieldRelatedLink", back_populates="poll")
    votes = relationship("Vote", back_populates="poll")
    poll_results_per_fraction = relationship("PollResultPerFraction", back_populates="poll")

    # One to One
    vote_result = relationship("VoteResult", back_populates="poll", uselist=False)
