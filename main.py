from fastapi import FastAPI, APIRouter
from uvicorn import run

from hotels import router as hotels_router

app = FastAPI()


app.include_router(hotels_router, tags=["Отели",])


if __name__ == "__main__":
    run("main:app", port=8000,  reload=True)
