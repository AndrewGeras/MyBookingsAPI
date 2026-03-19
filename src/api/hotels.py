from typing import Annotated

from fastapi import Query, Body, HTTPException, APIRouter
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from src.schemas.hotels import Hotel, HotelPATCH
from api.dependencies import PaginationDep

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геледжик", "name": "gelendzik"},
    {"id": 5, "title": "Москва", "name": "moskva"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "sankt-peterburg"},
    {"id": 8, "title": "Париж", "name": "pariz"},
]

router = APIRouter(prefix="/hotels")


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(default=None, description="идентификатор отеля"),
        title: str | None = Query(default=None, description="название отеля")):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if not hotels_:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Такой отель не найден")

    per_page, page = pagination.per_page, pagination.page
    num_pages = len(hotels_) // per_page + bool(len(hotels_) % per_page)

    if page > num_pages:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Превышено число страниц {num_pages}")

    from_ = per_page * (page - 1)
    to_ = per_page * page

    return hotels_[from_: to_]


@router.post("")
def create_hotel(hotel: Annotated[Hotel, Body(openapi_examples={
                        "normal": {
                            "summary": "Валидные данные",
                            "description": "Пример **валидных** данных отеля.",
                            "value": {"title": "Отель-Шмотель",
                                      "name": "hotel_shmotel"}
                        },
                        "invalid": {
                            "summary": "Невалидные данные",
                            "description": "Пример **невалидных** данных отеля.",
                            "value": {
                                "name": 123,
                                "price": 456,

                            },
                        },
                    }
                )
            ]
        ):
    global hotels

    hotels.append({"id": hotels[-1]["id"] + 1, "title": hotel.title, "name": hotel.name})
    return {"status": "OK"}


@router.put("/{hotel_id}", description="<strong>Полное</strong> редактирование данных об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"], hotel["name"] = hotel_data.title, hotel_data.name
            return hotel
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="not Found")


@router.patch("/{hotel_id}", description="<strong>Частичное</strong> редактирование данных об отеле")
def edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            return hotel
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="not Found")


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
