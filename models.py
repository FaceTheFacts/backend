from sqlalchemy import Column, String, Integer, ForeignKey, Text, Date
from sqlalchemy.orm import relationship

from database import Base


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String, unique=True)


class Poll(Base):
    __tablename__ = "poll"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    field_committees_id = Column(Integer, ForeignKey("committee.id"))
    field_intro = Column(Text)
    field_poll_date = Column(Date)
    # Many to One
    committee = relationship("Committee", back_populates="polls")


class Committee(Base):
    __tablename__ = "committee"
    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
