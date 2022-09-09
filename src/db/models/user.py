from src.db.connection import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
