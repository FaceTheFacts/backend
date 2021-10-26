from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class SidejobOrganization(Base):
    __tablename__ = "sidejob_organization"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    field_city_id = Column(Integer, ForeignKey("city.id"))
    field_country_id = Column(Integer, ForeignKey("country.id"))

    # Many to One
    city = relationship("City", back_populates="sidejob_organizations")
    country = relationship("Country", back_populates="sidejob_organizations")

    # One to Many
    sidejobs = relationship("Sidejob", back_populates="sidejob_organization")

    # Many to Many
    topics = relationship(
        "Topic",
        secondary="sidejob_organization_has_topic",
        back_populates="sidejob_organizations",
    )
