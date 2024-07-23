from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from db.base import Base
from booking.enum import BookingStatus
from auth.models import Auth
from books.models.book import Book


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('auth.id'))
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(BookingStatus), default=BookingStatus.ACTIVE, nullable=False)

    users = relationship(Auth, back_populates='booking')
    books = relationship(Book, back_populates='booking')
