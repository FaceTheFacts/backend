from sqlalchemy import Column, Integer, ForeignKey

from database import Base


class PollHasTopic(Base):
    __tablename__ = "poll_has_topic"

    poll_id = Column(Integer, ForeignKey("poll.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), primary_key=True)
