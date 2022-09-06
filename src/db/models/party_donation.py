from xmlrpc.client import Boolean
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.db.connection import Base

class PartyDonation(Base):
    __tablename__ = "party_donation"

    id = Column(Integer, primary_key=True)
    # entity_type = Column(String)
    # label = Column(String)
    # api_url = Column(String)
    party_id = Column(Integer, ForeignKey("party.id"))
    amount = Column(Integer)
    donor_name = Column(String)
    donor_address = Column(String)
    donor_zip = Column(Integer)
    donor_city = Column(String)
    donor_foreign = Column(Boolean)
    date = Column(Date)
