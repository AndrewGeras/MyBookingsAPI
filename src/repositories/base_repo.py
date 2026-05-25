from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.utils.handlers import ExcHandler, get_object_or_404


class BaseRepository:
    model: Base = None
    schema: BaseModel = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, **filters) -> [BaseModel]:
        query = select(self.model).filter_by(**filters)
        query_result = await self.session.scalars(query)
        return [self.schema.model_validate(model) for model in get_object_or_404(query_result.all())]

    async def get_all(self, *args, **kwargs) -> [BaseModel]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filters) -> BaseModel | None:
        query = select(self.model).filter_by(**filters)
        query_result = await self.session.scalars(query)
        model = query_result.one_or_none()
        return self.schema.model_validate(get_object_or_404(model))

    async def add(self, data: BaseModel) -> BaseModel | None:
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_stmt)
            model = result.scalars().one()
            return self.schema.model_validate(model)
        except Exception as err:
            ExcHandler().handle_exception(err)

    async def add_bulk(self, bulk_data: list[BaseModel]):
        add_stmt = insert(self.model).values([item.model_dump() for item in bulk_data])
        try:
            await self.session.execute(add_stmt)
        except Exception as err:
            ExcHandler().handle_exception(err)

    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> BaseModel | None:
        update_stmt = (update(self.model)
                       .filter_by(**filter_by)
                       .values(**data.model_dump(exclude_unset=exclude_unset))
                       .returning(self.model))
        result = await self.session.execute(update_stmt)
        model = result.scalars().one_or_none()
        return self.schema.model_validate(get_object_or_404(model))

    async def delete(self, **filter_by) -> BaseModel | None:
        delete_stmt = (delete(self.model)
                       .filter_by(**filter_by)
                       .returning(self.model))
        result = await self.session.execute(delete_stmt)
        model = result.scalars().one_or_none()
        return self.schema.model_validate(get_object_or_404(model))
