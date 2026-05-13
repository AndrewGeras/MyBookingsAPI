from datetime import date

from sqlalchemy import select
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

        print(query.compile(compile_kwargs={"literal_binds": True}))

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

        available_hotels = (get_available_by_date(date_from, date_to).cte("available_hotels"))

        query = (select(available_hotels,
                        hotels.c.title.label("hotel"),
                        hotels.c.location)
                 .select_from(available_hotels)
                 .join(hotels, hotels.c.id == available_hotels.c.hotel_id)
                 .order_by(available_hotels.c.hotel_id, available_hotels.c.price))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        query_result = await self.session.execute(query)
        return [AvailableHotels.model_validate(room) for room in query_result]
