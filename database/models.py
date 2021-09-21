from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


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
    displayName = Column(String, nullable=False)
    foregroundColor = Column(String, nullable=False)
    backgroundColor = Column(String, nullable=False)
    borderColor = Column(String)
