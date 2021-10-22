from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class ElectionProgram(Base):
    __tablename__ = "election_program"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    parliament_period_id = Column(Integer, ForeignKey("parliament_period.id"))
    party_id = Column(Integer, ForeignKey("party.id"))
    link_uri = Column(String)
    link_title = Column(String)
    link_option = Column(String)
    file = Column(String)
    parliament_period = relationship("ParliamentPeriod")
    party = relationship("Party")
