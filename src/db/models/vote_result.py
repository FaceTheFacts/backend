from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base, engine


class VoteResult(Base):
    __tablename__ = "vote_result"
    id = Column(Integer, primary_key=True)
    yes = Column(Integer, nullable=False)
    no = Column(Integer, nullable=False)
    abstain = Column(Integer, nullable=False)
    no_show = Column(Integer, nullable=False)
    poll_id = Column(Integer, ForeignKey("poll.id"))

    # One to One
    poll = relationship("Poll", back_populates="vote_result")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
