from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class ElectoralList(Base):
    __tablename__ = "electoral_list"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    name = Column(String)
    parliament_period_id = Column(Integer, ForeignKey("parliament_period.id"))
    parliament_period = relationship("ParliamentPeriod")
    electoral_data = relationship("ElectoralData", back_populates="electoral_list")
