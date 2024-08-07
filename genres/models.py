from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy import Column, Integer, String


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books_assoc = relationship('BookGenreAssociation', back_populates='genre')
