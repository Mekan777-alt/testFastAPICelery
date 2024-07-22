from booking.models import Booking
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

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