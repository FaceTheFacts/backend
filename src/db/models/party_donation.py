from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.db.connection import Base

class PartyDonation(Base):
    __tablename__ = "party_donation"

    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("party.id"))
    amount = Column(Float)
    date = Column(Date)
    party_donation_organization_id = Column(Integer, ForeignKey("party_donation_organization.id"))

    # Many to One
    party_donation_organization = relationship(
        "PartyDonationOrganization", back_populates="party_donations")