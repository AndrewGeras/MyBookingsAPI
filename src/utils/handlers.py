from typing import Sequence

from sqlalchemy.exc import IntegrityError
from psycopg.errors import Error
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from pydantic import BaseModel


def get_object_or_404(obj: BaseModel | Sequence | None):
    if not obj:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Информация по запросу не найдена")
    return obj


class ExcHandler:

    def handle_exception(self, exc: Exception):
        if isinstance(exc, IntegrityError):
            if isinstance(exc.orig, Error):
                message = exc.orig.diag.message_detail
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=message)
            raise exc
