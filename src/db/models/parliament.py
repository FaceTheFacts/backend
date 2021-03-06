from sqlalchemy import Column, String, Integer

from src.db.connection import Base


class Parliament(Base):
    __tablename__ = "parliament"

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String)
    label = Column(String)
    api_url = Column(String)
    abgeordnetenwatch_url = Column(String)
    label_external_long = Column(String)

    # current_project_id = Column(Integer, ForeignKey("parliament_period.id"))
    # parliament_period = relationship("ParliamentPeriod")
