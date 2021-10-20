from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from ..db.base import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String, unique=True)

    # One to Many
    sidejob_organizations = relationship("SidejobOrganization", back_populates="city")
    sidejobs = relationship("Sidejob", back_populates="city")
