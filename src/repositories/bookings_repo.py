from src.repositories.base_repo import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Bookings


class BookingsRepo(BaseRepository):
    model = BookingsORM
    schema = Bookings
