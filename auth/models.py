from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Auth(Base):
    __tablename__ = 'auth'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    booking = relationship('Booking', back_populates='users')
