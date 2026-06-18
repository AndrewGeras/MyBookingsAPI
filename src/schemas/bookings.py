from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingAddRequest):
    user_id: int
    price: Decimal


class BookingPatch(BaseModel):
    user_id: int | None = None
    room_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    price: Decimal | None = None


class Booking(BookingAdd):
    id: int
    create_at: datetime
