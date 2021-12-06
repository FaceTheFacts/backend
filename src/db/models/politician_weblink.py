from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base, engine


class PoliticianWeblink(Base):
    __tablename__ = "politician_weblink"

    id = Column(Integer(), primary_key=True)
    politician_id = Column(Integer, ForeignKey("politician.id"))
    link = Column(String)
    # Many to one
    politician = relationship("Politician", back_populates="weblinks")

if __name__ == "__main__":
    Base.metadata.create_all(engine)