from booking.enum import BookingStatus
from booking.models import Booking
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_conflicting_bookings(self, book_id: int, start_datetime: datetime, end_datetime: datetime):
        result = await self.db.execute(
            select(Booking).where(
                Booking.book_id == book_id,
                Booking.status == BookingStatus.ACTIVE,
                Booking.start_datetime < end_datetime,
                Booking.end_datetime > start_datetime
            )
        )
        return result.scalars().all()

    async def create_booking(self, booking: Booking):
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def get_booking(self, user_id: int):
        bookings = await self.db.execute(select(Booking).where(Booking.user_id == user_id))
        return bookings.scalars().all()

    async def get_booking_by_id(self, booking_id: int):
        booking = await self.db.execute(select(Booking).where(Booking.id == booking_id))
        return booking.scalar()

    async def update_booking(self, booking_id: int, status: BookingStatus, end_datetime: datetime = None):
        booking = await self.db.get(Booking, booking_id)

        if booking:
            booking.status = status

            if end_datetime:
                booking.end_datetime = end_datetime

            await self.db.commit()
            await self.db.refresh(booking)

        return booking

    async def get_active_bookings(self):
        bookings = await self.db.execute(select(Booking).where(Booking.status == BookingStatus.ACTIVE))
        return bookings.scalars().all()
