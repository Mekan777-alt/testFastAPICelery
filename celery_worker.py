from celery import Celery
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from booking.repositories import BookingRepository
from booking.enum import BookingStatus
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import asyncio
from celery.schedules import crontab

engine = create_async_engine(settings.pg_dsn)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

celery = Celery(__name__)

celery.conf.broker_url = f'redis://{settings.redis_host}:{settings.redis_port}'
celery.conf.result_backend = f'redis://{settings.redis_host}:{settings.redis_port}'


celery.conf.beat_schedule = {
    'check-bookings-every-5-minutes': {
        'task': 'celery_worker.check_and_release_bookings',
        'schedule': crontab(minute='*/2'),  # Каждые 2 минуты
    }
}


async def check_and_release_bookings_task():
    async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        booking_repo = BookingRepository(session)
        now = datetime.utcnow()
        bookings = await booking_repo.get_active_bookings()
        for booking in bookings:
            if booking.end_datetime < now:
                await booking_repo.update_booking(booking_id=booking.id, status=BookingStatus.RETURNED)


@celery.task
def check_and_release_bookings():
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()

    loop.run_until_complete(check_and_release_bookings_task())
