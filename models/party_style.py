from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# Maybe partystyle
class PartyStyle(Base):
    __tablename__ = "party_style"

    # party_id = Column(Integer, ForeignKey("party.id"))
    id = Column(Integer, primary_key=True)
    display_name = Column(String)
    foreground_color = Column(String)
    background_color = Column(String)
    border_color = Column(String)

    # # One to One
    # party = relationship("Party", back_populates="party")
