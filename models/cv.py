from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class CV(Base):
    __tablename__ = "cv"

    id = Column(Integer, primary_key=True, autoincrement=True)
    politician_id = Column(Integer, ForeignKey("politician.id"))
    raw_text = Column(String)
    short_description = Column(String)

    # Many to One
    politician = relationship("Politician", back_populates="cvs")

    # One to Many
    career_paths = relationship("CareerPath", back_populates="cv")
