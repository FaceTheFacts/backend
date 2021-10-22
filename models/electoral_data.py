from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class ElectoralData(Base):
    __tablename__ = "electoral_data"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    electoral_list_id = Column(Integer, ForeignKey("electoral_list.id"))
    list_position = Column(Integer)
    constituency_id = Column(Integer, ForeignKey("constituency.id"))
    constituency_result = Column(Float)
    constituency_result_count = Column(Integer)
    mandate_won = Column(String)
    electoral_list = relationship("ElectoralList", back_populates="electoral_data")
    constituency = relationship("Constituency", back_populates="electoral_data")

    # One to One
    candidacy_mandate = relationship(
        "CandidacyMandate", back_populates="electoral_data"
    )
