from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class CommitteeMembership(Base):
    __tablename__ = "committee_membership"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    committee_id = Column(Integer, ForeignKey("committee.id"))
    candidacy_mandate_id = Column(Integer, ForeignKey("candidacy_mandate.id"))
    committee_role = Column(String)

    # Many to One
    committee = relationship("Committee", back_populates="committee_memberships")
    candidacy_mandate = relationship(
        "CandidacyMandate", back_populates="committee_memberships"
    )
