from typing import Annotated
from datetime import date

from fastapi import APIRouter, Body, Query
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsAddRequest
from src.schemas.facilities import RoomFacilitiesAdd
from src.utils.examples_data import room_data
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Классы номеров отелей"])


@router.get("/{hotel_id}/rooms",
            description="<h2>Ручка для получения информации обо всех классах номеров, доступных для бронирования в отеле</h2>")
async def get_all_rooms(db: DBDep,
                        hotel_id: int,
                        date_from: Annotated[date, Query(example="2026-05-08")],
                        date_to: Annotated[date, Query(example="2026-05-10")]):
    rooms = await db.rooms.get_available(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return rooms if rooms else {"message": "Свободных номеров в данном отеле нет"}


@router.get("/{hotel_id}/rooms/{room_id}",
            description="<h2>Ручка для информации об определённом классу номеров в отеле</h2>")
async def get_specific_rooms(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms",
             status_code=HTTP_201_CREATED,
             description="<h2>Ручка для добавления информации о классе номеров в отель</h2>")
async def create_rooms(db: DBDep,
                       hotel_id: int,
                       rooms_data: Annotated[RoomsAddRequest, Body(openapi_examples=room_data)]):
    rooms_data_ = RoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    room = await db.rooms.add(rooms_data_)

    room_facilities_data = [RoomFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in rooms_data.facilities_ids]

    await db.room_facilities.add_bulk(room_facilities_data)
    await db.commit()
    return {"status": "OK", "details": room}


@router.put("/{hotel_id}/rooms/{room_id}",
            status_code=HTTP_204_NO_CONTENT,
            description="<h2>Ручка для <strong>полного</strong> изменения информации о классе номеров в отеле</h2>")
async def update_rooms(db: DBDep,
                       hotel_id: int,
                       room_id: int,
                       rooms_data: RoomsAddRequest):
    await db.rooms.edit(data=rooms_data, hotel_id=hotel_id, id=room_id)
    await db.commit()


@router.patch("/{hotel_id}/rooms/{room_id}",
              status_code=HTTP_204_NO_CONTENT,
              description="<h2>Ручка для <strong>частичного</strong> изменения информации о классе номеров в отеле</h2>")
async def edit_rooms(db: DBDep,
                     hotel_id: int,
                     room_id: int,
                     rooms_data: RoomsPatch):
    await db.rooms.edit(data=rooms_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.commit()


@router.delete("/{hotel_id}/rooms/{room_id}",
               status_code=HTTP_204_NO_CONTENT,
               description="<h2>Ручка для удаления информации о классе номеров в отеле</h2>")
async def delete_rooms(db: DBDep,
                       hotel_id: int,
                       room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
