from celery import Celery
from celery.schedules import crontab


celery_app = Celery(
    'booking_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    result_expires=3600,  # Срок действия результатов
)

celery_app.conf.beat_schedule = {
    'check_expired_bookings': {
        'task': 'tasks.check_expired_bookings',
        'schedule': 60.0,
    },
}


# Настройка периодических задач
celery_app.conf.beat_schedule = {
    'check-bookings': {
        'task': 'tasks.check_and_release_bookings',
        'schedule': crontab(minute='*/1'),  # Проверяем каждую минуту
    }
}