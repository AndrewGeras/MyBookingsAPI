from fastapi import Query, Body, HTTPException, APIRouter
from starlette.status import HTTP_404_NOT_FOUND

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]

router = APIRouter(prefix="/hotels")


@router.get("")
def get_hotels(id: int | None = Query(default=None, description="идентификатор отеля"),
               title: str | None = Query(default=None, description="название отеля")):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post("")
def create_hotel(title: str = Body(embed=True), name: str = Body(embed=True)):
    global hotels

    hotels.append({"id": hotels[-1]["id"] + 1, "title": title, "name": name})
    return {"status": "OK"}


@router.put("/{hotel_id}", description="<strong>Полное</strong> редактирование данных об отеле")
def update_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"], hotel["name"] = title, name
            return hotel
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="not Found")


@router.patch("/{hotel_id}", description="<strong>Частичное</strong> редактирование данных об отеле")
def edit_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            return hotel
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="not Found")


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
