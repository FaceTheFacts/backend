from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class FieldRelatedLink(Base):
    __tablename__ = "field_related_link"
    id = Column(Integer, primary_key=True, autoincrement=True)
    poll_id = Column(Integer, ForeignKey("poll.id"))
    uri = Column(String)
    title = Column(String)

    # Many to One
    poll = relationship("Poll", back_populates="field_related_links")
