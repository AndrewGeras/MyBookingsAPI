from decimal import Decimal

from pydantic import BaseModel

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: Decimal
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: Decimal
    quantity: int


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    hotel_id: int
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity: int | None = None


class Room(BaseModel):
    id: int
    title: str
    description: str | None
    price: Decimal
    facilities: list[Facility]


class RoomAvailable(Room):
    available_rooms: int
