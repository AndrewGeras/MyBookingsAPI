from pydantic import BaseModel


class Hotel(BaseModel):
    title: str
    name: str

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


class HotelPATCH(BaseModel):
    title: str | None = None
    name: str | None = None