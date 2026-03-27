from fastapi.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy import select

from src.repositories.base_repo import BaseRepository
from src.models.hotels import HotelsORM


class HotelsRepo(BaseRepository):
    model = HotelsORM

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
        hotels = query_result.all()

        if not hotels:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Отель по запросу не найден")

        return hotels

