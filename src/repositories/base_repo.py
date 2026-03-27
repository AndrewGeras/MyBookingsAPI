from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base


class BaseRepository:
    model: Base | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        query_result = await self.session.scalars(query)
        return query_result.all()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        query_result = await self.session.scalars(query)
        return query_result.one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        obj = await self.session.execute(add_stmt)
        return obj.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> None:
        update_stmt = (update(self.model)
                       .filter_by(**filter_by)
                       .values(**data.model_dump(exclude_unset=exclude_unset)))
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
