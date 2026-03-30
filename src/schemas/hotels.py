from pydantic import BaseModel, ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "title": "Название отеля",
    #                 "name": "hotel_slug"
    #             }
    #         ]
    #     }
    # }


class Hotel(HotelAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None