from typing import Annotated

from fastapi import Query, Body, HTTPException, APIRouter
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from sqlalchemy import insert, select

from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsORM

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
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="название отеля"),
        location: str | None = Query(default=None, description="локация отеля")):

    per_page = pagination.per_page or 3
    page = pagination.page

    async with async_session_maker() as session:
        query = select(HotelsORM).order_by(HotelsORM.id)
        if title:
            query = query.where(HotelsORM.title.ilike(f"%{title.strip()}%"))
        if location:
            query = query.where(HotelsORM.location.ilike(f"%{location.strip()}%"))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (page - 1))
        )

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        query_result = await session.scalars(query)

    hotels = query_result.all()

    if not hotels:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Отель по запросу не найден")

    # num_pages = len(hotels) // per_page + bool(len(hotels) % per_page)
    # print(hotels)
    #
    # if page > num_pages:
    #     raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Превышено число страниц {num_pages}")

    return hotels



@router.post("")
async def create_hotel(hotel: Annotated[Hotel, Body(openapi_examples={
                        "normal": {
                            "summary": "Валидные данные",
                            "description": "Пример **валидных** данных отеля.",
                            "value": {"title": "Отель-Шмотель",
                                      "location": "in_the_middle_of_nowhere"}
                        },
                        "invalid": {
                            "summary": "Невалидные данные",
                            "description": "Пример **невалидных** данных отеля.",
                            "value": {
                                "title": 123,
                                "location": 456,

                            },
                        },
                    }
                )
            ]
        ):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

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
