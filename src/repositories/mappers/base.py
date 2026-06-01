from pydantic import BaseModel

from src.database import Base


class DataMapper:
    db_model: Base | None = None
    schema: BaseModel | None = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistance_entity(cls, data: BaseModel):
        return cls.db_model(**data.model_dump())
