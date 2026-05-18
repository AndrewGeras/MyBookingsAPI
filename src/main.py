import sys
from pathlib import Path

from fastapi import FastAPI
from uvicorn import run

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as users_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router

app = FastAPI()


app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)


if __name__ == "__main__":
    run("src.main:app", port=8000,  reload=True)
