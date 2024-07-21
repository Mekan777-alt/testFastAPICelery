from sqlalchemy import Column, Integer, String

from db.base import Base


class Auth(Base):
    __tablename__ = 'auth'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
