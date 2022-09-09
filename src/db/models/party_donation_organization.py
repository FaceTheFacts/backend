from xmlrpc.client import Boolean
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base

class PartyDonationOrganization(Base):
    __tablename__ = "party_donation_organization"

    id = Column(Integer, primary_key=True)
    donor_name = Column(String)
    donor_address = Column(String)
    donor_zip = Column(Integer)
    donor_city = Column(String)
    donor_foreign = Column(Boolean)
    party_donation_id = Column(Integer,ForeignKey("party_donation.id"))

    # Many to One (Many donations to one org)
    party_donation = relationship(
        "PartyDonation", back_populates="party_donation_organization")