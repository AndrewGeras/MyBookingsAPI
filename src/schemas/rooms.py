from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: Decimal
    quantity: int
    facilities_ids: list[int] | None = None


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: Decimal
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class RoomsPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity: int | None = None


class Rooms(RoomsAdd):
    id: int


class AvailableRooms(BaseModel):
    room_id: int
    title: str
    description: str | None
    price: Decimal
    available_rooms: int

    model_config = ConfigDict(from_attributes=True)
