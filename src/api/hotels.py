from datetime import date
from typing import Annotated

from fastapi import Query, Body, APIRouter
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from fastapi_cache.decorator import cache

from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep, DBDep
from src.utils.examples_data import hotel_example, df_exmp, dt_exmp

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/all",
            description="<h2>Ручка для постраничного выбора отелей по названию и локации</h2>")
@cache(expire=30)
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="название отеля"),
        location: str | None = Query(default=None, description="локация отеля")
):
    per_page = pagination.per_page or 3
    page = pagination.page

    hotels = await db.hotels.get_all(title=title,
                                     location=location,
                                     limit=per_page,
                                     offset=per_page * (page - 1))
    return hotels


@router.get("",
            description="<h2>Ручка для получения информации об отелях с номерами, доступными для бронирования</h2>")
@cache(expire=30)
async def get_available_hotels(
        db: DBDep,
        pagination: PaginationDep,
        date_from: date = Query(description="дата заезда", default=df_exmp, examples=[df_exmp]),
        date_to: date = Query(description="дата выезда", default=dt_exmp, examples=[dt_exmp]),
        title: str | None = Query(default=None, description="название отеля"),
        location: str | None = Query(default=None, description="локация отеля")
):
    per_page = pagination.per_page or 3
    page = pagination.page

    hotels = await db.hotels.get_available(title=title,
                                           location=location,
                                           limit=per_page,
                                           offset=per_page * (page - 1),
                                           date_from=date_from,
                                           date_to=date_to)
    return hotels


@router.get("/{hotel_id}",
            description="<h2>Ручка для получения одного отеля по его ID</h2>")
async def get_hotel(db: DBDep, hotel_id: int):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return hotel


@router.post("",
             status_code=HTTP_201_CREATED,
             description="<h2>Ручка для добавления нового отеля</h2>")
async def create_hotel(db: DBDep,
                       hotel: Annotated[HotelAdd, Body(openapi_examples=hotel_example)]):
    await db.hotels.add(hotel)
    await db.commit()


@router.put("/{hotel_id}",
            status_code=HTTP_204_NO_CONTENT,
            description="<h2>Ручка для <strong>полного</strong> редактирование данных об отеле</h2>")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()


@router.patch("/{hotel_id}",
              status_code=HTTP_204_NO_CONTENT,
              description="<h2>Ручка для <strong>частичного</strong> редактирование данных об отеле</h2>")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()


@router.delete("/{hotel_id}",
               status_code=HTTP_204_NO_CONTENT,
               description="<h2>Ручка для удаления отеля по ID</h2>")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
