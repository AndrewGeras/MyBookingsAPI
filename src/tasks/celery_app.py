from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_inst = Celery("tasks", broker=settings.BROCKER_URL, include=["src.tasks.tasks"])

celery_inst.conf.beat_schedule = {
    "remind_bookings_today_checkin_schedule": {
        "task": "bookings_today_checkin",
        "schedule": crontab.from_string("45 13 * * *"),  # crontab guru
    }
}
