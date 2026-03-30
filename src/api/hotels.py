from typing import Annotated

from fastapi import Query, Body, APIRouter, HTTPException
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels_repo import HotelsRepo
from src.api.utils import get_object_or_404


router = APIRouter(prefix="/hotels")


@router.get("",
            description="<h2>Метод постраничного выбора отелей по названию и локации</h2>")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="название отеля"),
        location: str | None = Query(default=None, description="локация отеля")
):

    per_page = pagination.per_page or 3
    page = pagination.page

    async with async_session_maker() as session:
        hotels = await HotelsRepo(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (page - 1)
        )
        return get_object_or_404(hotels, "hotel")



@router.get("/{hotel_id}",
            description="<h2>Метод для получения одного отеля по его ID</h2>")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepo(session).get_one_or_none(id=hotel_id)
        return get_object_or_404(hotel, "hotel")



@router.post("",
             status_code=HTTP_201_CREATED,
             description="<h2>Метод для добавления нового отеля</h2>")
async def create_hotel(hotel: Annotated[HotelAdd, Body(openapi_examples={
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
        hotel = await HotelsRepo(session).add(hotel)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
            status_code=HTTP_204_NO_CONTENT,
            description="<h2><strong>Полное</strong> редактирование данных об отеле</h2>")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        hotel = await HotelsRepo(session).edit(data=hotel_data, id=hotel_id)
        get_object_or_404(hotel, "hotel")
        await session.commit()


@router.patch("/{hotel_id}",
              status_code=HTTP_204_NO_CONTENT,
              description="<h2><strong>Частичное</strong> редактирование данных об отеле</h2>")
async def edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        hotel = await HotelsRepo(session).edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        get_object_or_404(hotel, "hotel")
        await session.commit()


@router.delete("/{hotel_id}",
               status_code=HTTP_204_NO_CONTENT,
               description="<h2>Метод для удаления отеля по ID</h2>")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepo(session).delete(id=hotel_id)
        get_object_or_404(hotel, "hotel")
        await session.commit()