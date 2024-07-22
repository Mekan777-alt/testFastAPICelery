from typing import List

from fastapi import HTTPException
from starlette import status
from booking.repositories import BookingRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from booking.schemas import BookingCreate
from booking.models import Booking
from booking.enum import BookingStatus


class BookingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.booking_repository = BookingRepository(db)

    async def create_booking(self, booking: BookingCreate, user_id: int, book_id: int):

        conflict_booking = await self.db.execute(
            select(Booking).where(
                Booking.book_id == book_id,
                Booking.status == BookingStatus.ACTIVE,
                Booking.start_date <= booking.start_date,
            )
        )

        if conflict_booking.scalar():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Книга уже забронирована на указанные даты."
            )

        new_booking = Booking(
            book_id=book_id,
            user_id=user_id,
            start_date=booking.start_date,
            end_date=booking.end_date,
        )
        return await self.booking_repository.create_booking(new_booking)

    async def get_bookings_user(self, user_id: int) -> List[Booking]:
        return await self.booking_repository.get_booking(user_id)

    async def get_bookings_id(self, booking_id: int):
        return await self.booking_repository.get_booking_by_id(booking_id)

    async def return_booking(self, booking_id: int):
        booking = await self.booking_repository.update_booking(booking_id, BookingStatus.RETURNED)

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бронирование не найдено"
            )

        return booking
