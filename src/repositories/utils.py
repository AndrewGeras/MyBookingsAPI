from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def get_available_by_date(date_from: date,
                          date_to: date,
                          hotel_id: int | None = None):

    booked_rooms_cte = (select(BookingsORM.room_id, func.count().label("rooms_count"))
                        .select_from(BookingsORM)
                        .filter(BookingsORM.date_to > date_from, BookingsORM.date_from < date_to)
                        .group_by(BookingsORM.room_id)
                        .cte("booked_rooms"))

    available_rooms_cte = (select(RoomsORM,
                                  (RoomsORM.quantity - func.coalesce(booked_rooms_cte.c.rooms_count, 0))
                                  .label("available_rooms"))
                           .select_from(RoomsORM)
                           .outerjoin(booked_rooms_cte, RoomsORM.id == booked_rooms_cte.c.room_id)
                           .cte("available_rooms"))

    rooms_at_hotel = select(RoomsORM.id).select_from(RoomsORM)

    if not hotel_id is None:
        rooms_at_hotel = rooms_at_hotel.filter_by(hotel_id=hotel_id)

    subq = rooms_at_hotel.subquery()

    query = (select(available_rooms_cte)
            .filter(available_rooms_cte.c.available_rooms > 0,
                    available_rooms_cte.c.id.in_(select(subq)))
        )

    return query
