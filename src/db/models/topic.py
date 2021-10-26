from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    abgeordnetenwatch_url = Column(String)
    description = Column(String)
    parent_id = Column(Integer(), ForeignKey("topic.id"))
    committees = relationship(
        "Committee", secondary="committee_has_topic", back_populates="topics"
    )

    # Many to Many
    polls = relationship("Poll", secondary="poll_has_topic", back_populates="topics")
    sidejob_organizations = relationship(
        "SidejobOrganization",
        secondary="sidejob_organization_has_topic",
        back_populates="topics",
    )

    # Many to Many
    sidejobs = relationship(
        "Sidejob",
        secondary="sidejob_has_topic",
        back_populates="topics",
    )
    position_statements = relationship("PositionStatement", back_populates="topics")
