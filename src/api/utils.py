from fastapi import HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_404_NOT_FOUND


def get_object_or_404(obj: BaseModel | None, obj_name: str):
    if not obj:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"{obj_name} is not found")
    return obj