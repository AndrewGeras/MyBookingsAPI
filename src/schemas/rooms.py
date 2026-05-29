from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.schemas.facilities import Facility


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


class Rooms(BaseModel):
    id: int
    title: str
    description: str | None
    price: Decimal
    facilities: list[Facility]

    model_config = ConfigDict(from_attributes=True)


class RoomsAvailable(Rooms):
    available_rooms: int