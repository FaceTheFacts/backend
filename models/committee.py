from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Committee(Base):
    __tablename__ = "committee"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    field_legislature_id = Column(Integer(), ForeignKey("parliament_period.id"))
    parliament_period = relationship("ParliamentPeriod", backref="parliament_period")
    topics = relationship(
        "Topic", secondary="committee_has_topic", back_populates="committees"
    )

    # One to Many
    committee_memberships = relationship(
        "CommitteeMembership", back_populates="committee"
    )
    polls = relationship("Poll", back_populates="committee")
