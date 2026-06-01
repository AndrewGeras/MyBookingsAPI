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


class Booking(BookingAdd):
    id: int
    create_at: datetime
