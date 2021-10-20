from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from ..db.base import Base


class CandidacyMandate(Base):
    __tablename__ = "candidacy_mandate"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    id_external_administration = Column(String)
    id_external_administration_description = Column(String)
    type = Column(String)
    parliament_period_id = Column(Integer, ForeignKey("parliament_period.id"))
    politician_id = Column(Integer, ForeignKey("politician.id"))
    party_id = Column(Integer, ForeignKey("party.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    info = Column(String)
    electoral_data_id = Column(Integer, ForeignKey("electoral_data.id"))
    fraction_membership_id = Column(Integer, ForeignKey("fraction_membership.id"))

    # Many to One
    parliament_period = relationship(
        "ParliamentPeriod", back_populates="candidacy_mandates"
    )
    politician = relationship("Politician", back_populates="candidacy_mandates")
    party = relationship("Party", back_populates="candidacy_mandates")

    # One to One
    electoral_data = relationship(
        "ElectoralData", back_populates="candidacy_mandate", uselist=False
    )
    fraction_membership = relationship(
        "FractionMembership", back_populates="candidacy_mandate", uselist=False
    )

    # One to Many
    committee_memberships = relationship(
        "CommitteeMembership", back_populates="candidacy_mandate"
    )
    votes = relationship("Vote", back_populates="candidacy_mandate")

    # Many to Many
    sidejobs = relationship(
        "Sidejob",
        secondary="sidejob_has_mandate",
        back_populates="candidacy_mandates",
    )
