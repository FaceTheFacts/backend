from sqlalchemy import Column, Integer, ForeignKey

from src.db.connection import Base


class CommitteeHasTopic(Base):
    __tablename__ = "committee_has_topic"

    committee_id = Column(Integer(), ForeignKey("committee.id"), primary_key=True)
    topic_id = Column(Integer(), ForeignKey("topic.id"), primary_key=True)
