from typing import Sequence
from fastapi import HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_404_NOT_FOUND


def get_object_or_404(obj: BaseModel | Sequence | None):
    if not obj:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Информация по запросу не найдена")
    return obj
