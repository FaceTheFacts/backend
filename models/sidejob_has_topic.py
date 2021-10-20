from sqlalchemy import Column, Integer, ForeignKey

from ..db.base import Base


class SidejobHasTopic(Base):
    __tablename__ = "sidejob_has_topic"

    sidejob_id = Column(Integer, ForeignKey("sidejob.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), primary_key=True)
