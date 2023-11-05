from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Sidejob(Base):
    __tablename__ = "sidejob"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    job_title_extra = Column(String)
    additional_information = Column(String)
    category = Column(String)
    income_level = Column(String)
    interval = Column(String)
    data_change_date = Column(Date)
    created = Column(Integer)
    sidejob_organization_id = Column(Integer, ForeignKey("sidejob_organization.id"))
    field_city_id = Column(Integer, ForeignKey("city.id"))
    field_country_id = Column(Integer, ForeignKey("country.id"))
    income = Column(Float)
    # Many to One
    sidejob_organization = relationship(
        "SidejobOrganization", back_populates="sidejobs"
    )
    city = relationship("City", back_populates="sidejobs")
    country = relationship("Country", back_populates="sidejobs")

    # Many to Many
    candidacy_mandates = relationship(
        "CandidacyMandate",
        secondary="sidejob_has_mandate",
        back_populates="sidejobs",
    )
    topics = relationship(
        "Topic",
        secondary="sidejob_has_topic",
        back_populates="sidejobs",
    )
