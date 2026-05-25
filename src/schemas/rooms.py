from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: Decimal
    quantity: int
    facilities_ids: list[int] = []


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: Decimal
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class RoomsPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomsPatch(BaseModel):
    hotel_id: int
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity: int | None = None

    model_config = ConfigDict(from_attributes=True)


class Rooms(RoomsAdd):
    id: int


class AvailableRooms(BaseModel):
    room_id: int
    title: str
    description: str | None
    price: Decimal
    available_rooms: int

    model_config = ConfigDict(from_attributes=True)
