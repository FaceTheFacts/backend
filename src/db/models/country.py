from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String, unique=True)

    # One to Many
    sidejob_organizations = relationship(
        "SidejobOrganization", back_populates="country"
    )

    # One to Many
    sidejobs = relationship("Sidejob", back_populates="country")
