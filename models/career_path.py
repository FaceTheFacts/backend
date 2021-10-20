from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..db.base import Base


class CareerPath(Base):
    __tablename__ = "career_path"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cv_id = Column(Integer, ForeignKey("cv.id"))
    raw_text = Column(String)
    label = Column(String)
    period = Column(String)
    # Many to One
    cv = relationship("CV", back_populates="career_paths")
