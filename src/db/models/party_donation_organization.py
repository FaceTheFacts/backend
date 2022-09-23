from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class PartyDonationOrganization(Base):
    __tablename__ = "party_donation_organization"

    id = Column(Integer, primary_key=True)
    donor_name = Column(String)
    donor_address = Column(String)
    donor_zip = Column(String)
    donor_city = Column(String)
    donor_foreign = Column(Boolean)

    # One to Many
    party_donations = relationship(
        "PartyDonation", back_populates="party_donation_organization"
    )
