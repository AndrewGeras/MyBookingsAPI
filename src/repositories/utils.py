from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def get_available_by_date(date_from: date,
                date_to: date,
                hotel_id: int | None = None):

    booked_rooms = (select(BookingsORM.room_id, func.count().label("rooms_count"))
                            .select_from(BookingsORM)
                            .filter(BookingsORM.date_to > date_from, BookingsORM.date_from < date_to)
                            .group_by(BookingsORM.room_id)
                            .cte("booked_rooms"))
    available_rooms = (select(RoomsORM,
                              (RoomsORM.quantity - func.coalesce(booked_rooms.c.rooms_count, 0))
                              .label("available_rooms"))
                       .select_from(RoomsORM)
                       .outerjoin(booked_rooms, RoomsORM.id == booked_rooms.c.room_id)
                       .cte("available_rooms"))

    query = (
        select(available_rooms.c.id.label("room_id"),
               available_rooms.c.hotel_id,
               available_rooms.c.title,
               available_rooms.c.description,
               available_rooms.c.price,
               available_rooms.c.available_rooms)
        .select_from(available_rooms)
        .filter(available_rooms.c.available_rooms > 0)
    )

    if not hotel_id is None:
        return query.filter_by(hotel_id=hotel_id)
    return query
