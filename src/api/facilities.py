from typing import Annotated

from fastapi import APIRouter, Body
from starlette.status import HTTP_201_CREATED
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", description="<h2>Ручка для получения списка всех удобств</h2>")
@cache(expire=30)
async def get_all_facilities(db: DBDep):
    facilities = await db.facilities.get_all()
    return facilities


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    description="<h2>Ручка для добавления удобств</h2>",
)
async def add_facility(db: DBDep, title: Annotated[FacilityAdd, Body()]):
    facility = await db.facilities.add(title)
    await db.commit()
    # task1.delay(5)
    return {"status": "OK", "details": facility}
