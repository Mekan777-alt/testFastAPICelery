from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from books.models import Book
from db.base import Base
from genres.models import Genre


class BookGenreAssociation(Base):
    __tablename__ = 'book_genre_association'

    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)

    genre = relationship(Genre, back_populates='books')
    books = relationship(Book, back_populates='genres')
