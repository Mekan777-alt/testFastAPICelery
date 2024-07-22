from sqlalchemy.orm import relationship
from authors.models import Authors
from db.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    pages = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    authors = relationship(Authors, back_populates='books')
    books_assoc = relationship('BookGenreAssociation', back_populates='books')
    booking = relationship('Booking', back_populates='books')
