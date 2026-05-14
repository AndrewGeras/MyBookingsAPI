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

    available_rooms = (select(RoomsORM.id.label("room_id"),
                              RoomsORM.hotel_id,
                              RoomsORM.title,
                              RoomsORM.price,
                              RoomsORM.description,
                              (RoomsORM.quantity - func.coalesce(booked_rooms.c.rooms_count, 0))
                              .label("available_rooms"))
                       .select_from(RoomsORM)
                       .outerjoin(booked_rooms, RoomsORM.id == booked_rooms.c.room_id)
                       .cte("available_rooms"))

    rooms_at_hotel = (select(RoomsORM.id)
                      .select_from(RoomsORM)
                      .filter_by(hotel_id=hotel_id)
                      .subquery("rooms_at_hotel"))

    query = (
        select(available_rooms)
        .filter(available_rooms.c.available_rooms > 0)
    )

    if not hotel_id is None:
        query = (
            select(available_rooms)
            .filter(available_rooms.c.available_rooms > 0,
                    available_rooms.c.room_id.in_(rooms_at_hotel))
        )
    return query
