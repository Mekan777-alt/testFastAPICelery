from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from db.base import Base
from booking.enum import BookingStatus


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('auth.id'))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(SQLAlchemyEnum(BookingStatus), default=BookingStatus.ACTIVE)

    users = relationship('Auth', back_populates='booking')
    books = relationship('Book', back_populates='booking')

    __table_args__ = (
        UniqueConstraint('book_id', 'start_date', name='unique_booking_start_date'),
        UniqueConstraint('book_id', 'end_date', name='unique_booking_end_date'),
    )
