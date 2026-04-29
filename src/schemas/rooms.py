from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: Decimal
    quantity: int


class RoomsAdd(RoomsAddRequest):
    hotel_id: int


class RoomsPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity: int | None = None


class Rooms(RoomsAdd):
    id: int
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)