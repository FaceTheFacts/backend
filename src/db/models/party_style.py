from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


# Maybe partystyle
class PartyStyle(Base):
    __tablename__ = "party_style"

    # party_id = Column(Integer, ForeignKey("party.id"))
    id = Column(Integer, primary_key=True)
    display_name = Column(String)
    foreground_color = Column(String)
    background_color = Column(String)
    border_color = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "display_name": self.display_name,
            "foreground_color": self.foreground_color,
            "background_color": self.background_color,
            "border_color": self.border_color,
        }

    # # One to One
    party = relationship("Party", back_populates="party_style")
