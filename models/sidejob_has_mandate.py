from sqlalchemy import Column, Integer, ForeignKey

from database import Base


class SidejobHasMandate(Base):
    __tablename__ = "sidejob_has_mandate"
    sidejob_id = Column(Integer, ForeignKey("sidejob.id"), primary_key=True)
    candidacy_mandate_id = Column(
        Integer, ForeignKey("candidacy_mandate.id"), primary_key=True
    )
