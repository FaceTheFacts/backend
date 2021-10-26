from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class PoliticianWeblink(Base):
    __tablename__ = "politician_weblink"

    id = Column(Integer(), primary_key=True)
    politician_id = Column(Integer, ForeignKey("politician.id"))
    link = Column(String)

    politician = relationship("Politician", back_populates="weblinks")
