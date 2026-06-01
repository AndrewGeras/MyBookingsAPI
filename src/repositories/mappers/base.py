from typing import TypeVar, Generic

from pydantic import BaseModel

from src.database import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=[BaseModel, dict])


class DataMapper(Generic[DBModelType, SchemaType]):
    db_model: type[DBModelType]
    schema: type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, data: DBModelType) -> SchemaType:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistance_entity(cls, data: SchemaType) -> DBModelType:
        return cls.db_model(**data.model_dump())
