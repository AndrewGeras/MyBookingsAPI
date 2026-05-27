from datetime import date

from sqlalchemy import select, func
from pydantic import BaseModel

from src.repositories.base_repo import BaseRepository
from src.repositories.utils import get_available_by_date
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, AvailableHotels
from src.utils.handlers import get_object_or_404


class HotelsRepo(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(
            self,
            title: str,
            location: str,
            limit: int,
            offset: int
    ):
        query = select(self.model).order_by(self.model.id)
        if title:
            query = query.where(self.model.title.ilike(f"%{title.strip()}%"))
        if location:
            query = query.where(self.model.location.ilike(f"%{location.strip()}%"))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        query_result = await self.session.scalars(query)

        hotels = [self.schema.model_validate(model, from_attributes=True) for model in
                  get_object_or_404(query_result.all())]

        return hotels

    async def get_available(self,
                            title: str,
                            location: str,
                            limit: int,
                            offset: int,
                            date_from: date,
                            date_to: date) -> [BaseModel]:
        hotels = select(self.model).cte("hotels")
        if title:
            hotels = select(self.model).where(self.model.title.ilike(f"%{title.strip()}%")).cte("hotels")
        if location:
            hotels = select(self.model).where(self.model.location.ilike(f"%{location.strip()}%")).cte("hotels")

        available_rooms_at_hotel = (get_available_by_date(date_from, date_to).cte("available_rooms_at_hotel"))

        query = (select(hotels,
                        func.sum(available_rooms_at_hotel.c.available_rooms).label("available_rooms"),
                        func.min(available_rooms_at_hotel.c.price).label("price_from"))
                 .select_from(hotels)
                 .join(available_rooms_at_hotel, hotels.c.id == available_rooms_at_hotel.c.hotel_id)
                 .group_by(hotels)
                 .limit(limit)
                 .offset(offset))
        query_result = await self.session.execute(query)
        return [AvailableHotels.model_validate(hotel) for hotel in query_result]
