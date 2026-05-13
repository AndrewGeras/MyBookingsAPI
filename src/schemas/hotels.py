from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None


class AvailableHotels(BaseModel):
    hotel_id: int
    hotel: str
    location: str
    room_id: int
    title: str
    description: str | None
    price: Decimal
    available_rooms: int

    model_config = ConfigDict(from_attributes=True)
