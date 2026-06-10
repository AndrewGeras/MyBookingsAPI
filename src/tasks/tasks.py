import os
from time import sleep

from src.tasks.celery_app import celery_inst
from PIL import Image


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
