from core.celery import celery_app
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from booking.repositories import BookingRepository
from booking.enum import BookingStatus
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import asyncio

engine = create_async_engine(settings.pg_dsn)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@celery_app.task
def check_and_release_bookings():
    async def async_check():
        async with async_session_maker() as session:
            booking_repo = BookingRepository(session)
            now = datetime.now()

            bookings = await booking_repo.get_active_bookings()

            for booking in bookings:

                if booking.end_datetime <= now:

                    await booking_repo.update_booking(booking_id=booking.id, status=BookingStatus.RETURNED)

    asyncio.run(async_check())
