from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class FractionMembership(Base):
    __tablename__ = "fraction_membership"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    fraction_id = Column(Integer, ForeignKey("fraction.id"))
    valid_from = Column(String)
    valid_until = Column(String)
    fraction = relationship("Fraction", back_populates="fraction_membership")

    # One to One
    candidacy_mandate = relationship(
        "CandidacyMandate", back_populates="fraction_membership"
    )
