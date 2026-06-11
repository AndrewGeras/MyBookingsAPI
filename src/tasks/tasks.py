import os
from time import sleep

import asyncio
from PIL import Image

from src.tasks.celery_app import celery_inst
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@celery_inst.task
def task1(s: int):
    sleep(s)
    print("Task is complete")


@celery_inst.task()
def create_image_thumbnail(image_name):
    path, ext = os.path.splitext(image_name)
    for size in (128, 800, 1200):
        sleep(5)
        with Image.open(image_name) as image:
            image.thumbnail((size, size))
            image.save(f"{path}_{size}px{ext}")
        print(f"image {size}px is created")


async def get_bookings_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_inst.task(name="bookings_today_checkin")
def remind_about_booking_today_checkin():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_bookings_today_checkin_helper())
