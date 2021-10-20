from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..db.base import Base


class Fraction(Base):
    __tablename__ = "fraction"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    full_name = Column(String)
    short_name = Column(String)
    legislature_id = Column(Integer, ForeignKey("parliament_period.id"))
    parliament_period = relationship("ParliamentPeriod")
    fraction_membership = relationship("FractionMembership", back_populates="fraction")

    # One to Many
    votes = relationship("Vote", back_populates="fraction")
