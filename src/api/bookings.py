from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAdd, BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("/{room_id}",
             status_code=HTTP_201_CREATED,
             description="<h2>Ручка для добавления бронирования номера в отеле</h2>")
async def book_room(db: DBDep,
                    user_id: UserIdDep,
                    booking_data: BookingAddRequest
                    ):

    room = await db.rooms.get_one_or_none(id=booking_data.room_id)

    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room.price,
        **booking_data.model_dump()
    )

    booking_details = await db.bookings.add_booking(_booking_data)
    await db.commit()
    return {"message": "Номер успешно забронирован", "details": booking_details}
