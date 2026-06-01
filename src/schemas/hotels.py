from decimal import Decimal

from pydantic import BaseModel


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None


class AvailableHotel(BaseModel):
    id: int
    title: str
    location: str
    price_from: Decimal
    available_rooms: int
