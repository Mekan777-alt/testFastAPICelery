from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship


class Authors(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String)

    books = relationship('Book', back_populates='authors')
