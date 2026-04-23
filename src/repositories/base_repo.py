from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.services.exeption_handlers import ExcHandler


class BaseRepository:
    model: Base = None
    schema: BaseModel = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *args, **kwargs) -> [BaseModel]:
        query = select(self.model)
        query_result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in query_result.scalars().all()]

    async def get_one_or_none(self, **filters) -> BaseModel | None:
        query = select(self.model).filter_by(**filters)
        query_result = await self.session.scalars(query)
        model = query_result.one_or_none()
        if model:
            return self.schema.model_validate(model)

    async def add(self, data: BaseModel) -> BaseModel | None:
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_stmt)
        except Exception as err:
            ExcHandler().handle_exception(err)

        model = result.scalars().one()
        return self.schema.model_validate(model)


    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> BaseModel | None:
        update_stmt = (update(self.model)
                       .filter_by(**filter_by)
                       .values(**data.model_dump(exclude_unset=exclude_unset))
                       .returning(self.model))
        result = await self.session.execute(update_stmt)
        model = result.scalars().one_or_none()
        if model:
            return self.schema.model_validate(model)

    async def delete(self, **filter_by) -> BaseModel | None:
        delete_stmt = (delete(self.model)
                       .filter_by(**filter_by)
                       .returning(self.model))
        result = await self.session.execute(delete_stmt)
        model = result.scalars().one_or_none()
        if model:
            return self.schema.model_validate(model)
