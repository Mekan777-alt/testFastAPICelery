from datetime import date, datetime
from typing import List

from fastapi import HTTPException
from starlette import status
from booking.repositories import BookingRepository
from sqlalchemy.ext.asyncio import AsyncSession
from books.repositories.book_repositories import BookRepository
from booking.schemas import BookingCreate
from booking.models import Booking
from booking.enum import BookingStatus


class BookingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.booking_repository = BookingRepository(db)
        self.books_repository = BookRepository(db)

    async def create_booking(self, booking: BookingCreate, user_id: int, book_id: int):
        book = await self.books_repository.get_book(book_id)
        if not book:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book does not exist",
            )

        if booking.start_datetime < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дата начала бронирования не может быть задним числом."
            )

        conflicting_bookings = await self.booking_repository.get_conflicting_bookings(
            book_id=book_id,
            start_datetime=booking.start_datetime,
            end_datetime=booking.end_datetime
        )

        if conflicting_bookings:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Книга уже забронирована на указанные даты."
            )

        new_booking = Booking(
            book_id=book_id,
            user_id=user_id,
            start_datetime=booking.start_datetime,
            end_datetime=booking.end_datetime,
            status=BookingStatus.ACTIVE
        )
        return await self.booking_repository.create_booking(new_booking)

    async def get_bookings_user(self, user_id: int) -> List[Booking]:
        return await self.booking_repository.get_booking(user_id)

    async def get_bookings_id(self, booking_id: int):
        booking = await self.booking_repository.get_booking_by_id(booking_id)

        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        return booking

    async def return_booking(self, booking_id: int):
        booking = await self.booking_repository.update_booking(booking_id, BookingStatus.RETURNED,
                                                               end_datetime=datetime.now())

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бронирование не найдено"
            )

        return booking

    async def cancel_booking(self, booking_id: int):
        booking = await self.booking_repository.update_booking(booking_id, BookingStatus.CANCELLED)

        if not booking:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        return booking
