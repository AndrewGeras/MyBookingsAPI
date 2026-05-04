from sqlalchemy import select

from src.repositories.base_repo import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel
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
