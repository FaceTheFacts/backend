from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class PositionStatement(Base):
    __tablename__ = "position_statement"

    # id has the following structure parliament_period + statement_number (130 + 1 -> 1301)
    id = Column(Integer(), primary_key=True)
    statement = Column(String)
    topic_id = Column(Integer, ForeignKey("topic.id"))
    topics = relationship("Topic", back_populates="position_statements")
    positions = relationship("Position", back_populates="position_statements")
