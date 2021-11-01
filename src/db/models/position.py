from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Position(Base):
    __tablename__ = "position"

    # id has the following structure: parliament_period * 10 + statement_number (130 * 10 + 1 = 1301)
    id = Column(BigInteger, primary_key=True)
    position = Column(String)
    reason = Column(String())
    politician_id = Column(Integer, ForeignKey("politician.id"))
    parliament_period_id = Column(Integer, ForeignKey("parliament_period.id"))
    position_statement_id = Column(Integer, ForeignKey("position_statement.id"))

    politicians = relationship("Politician", back_populates="positions")
    parliament_periods = relationship("ParliamentPeriod", back_populates="positions")
    position_statements = relationship("PositionStatement", back_populates="positions")
