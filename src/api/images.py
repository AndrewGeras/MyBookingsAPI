import os
from shutil import copyfileobj

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import create_image_thumbnail

router = APIRouter(prefix="/images", tags=["Изображения"])



@router.post("")
def upload_image(file: UploadFile):
    image_path = os.path.join(os.getcwd(), os.path.normpath("static/images/"))
    image_name = os.path.join(image_path, file.filename)

    with open(image_name, "wb+") as new_file:
        copyfileobj(file.file, new_file)

    create_image_thumbnail.delay(image_name)
