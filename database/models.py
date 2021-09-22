from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Politician(Base):
    __tablename__ = "politician"
    id = Column(Integer, primary_key=True)
    popularity = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    partyId = Column(Integer, ForeignKey("party.id"))
    party = relationship("Party")


class Party(Base):
    __tablename__ = "party"
    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String, nullable=False)
    foreground_color = Column(String, nullable=False)
    background_color = Column(String, nullable=False)
    border_color = Column(String)
