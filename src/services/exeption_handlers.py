from sqlalchemy.exc import IntegrityError
from psycopg.errors import Error
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class ExcHandler:

    def handle_exception(self, exc: Exception):
        if isinstance(exc, IntegrityError):
            if isinstance(exc.orig, Error):
                message = exc.orig.diag.message_detail
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=message)
            raise exc

    def __call__(self, exc: Exception):
        self.handle_exception(exc)

