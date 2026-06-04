import json
from typing import Annotated

from fastapi import APIRouter, Body
from starlette.status import HTTP_201_CREATED

from src.init import redis_manager
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("",
            description="<h2>Ручка для получения списка всех удобств</h2>")
async def get_all_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if facilities_from_cache:
        return json.loads(facilities_from_cache)
    facilities = await db.facilities.get_all()
    facilities_for_cache = json.dumps([facility.model_dump() for facility in facilities])
    await redis_manager.set("facilities", facilities_for_cache, expire=60)
    return facilities


@router.post("",
             status_code=HTTP_201_CREATED,
             description="<h2>Ручка для добавления удобств</h2>")
async def add_facility(db: DBDep,
                       title: Annotated[FacilityAdd, Body()]):
    facility = await db.facilities.add(title)
    await db.commit()
    return {"status": "OK", "details": facility}
