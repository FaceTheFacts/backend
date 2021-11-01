from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Constituency(Base):
    __tablename__ = "constituency"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    name = Column(String)
    number = Column(Integer)
    # TODO: parliament_period might only be a query parameter
    parliament_period_id = Column(Integer, ForeignKey("parliament_period.id"))
    parliament_period = relationship("ParliamentPeriod")
    electoral_data = relationship("ElectoralData", back_populates="constituency")
    # One to Many
    zip_codes = relationship("ZipCode", back_populates="constituency")
