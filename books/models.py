from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class BookGenreAssociation(Base):
    __tablename__ = 'book_genre_association'

    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)

    genre = relationship('Genre', back_populates='books')
    book = relationship('Book', back_populates='genres')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    pages = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship('User', back_populates='books')
    genres = relationship('BookGenreAssociation', back_populates='book')


