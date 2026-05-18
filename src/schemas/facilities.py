from pydantic import BaseModel, ConfigDict

class FacilityAdd(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)


class Facility(FacilityAdd):
    id: int


class RoomFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilities(RoomFacilitiesAdd):
    id: int
