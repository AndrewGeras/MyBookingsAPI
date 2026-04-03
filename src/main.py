import sys
from pathlib import Path

from fastapi import FastAPI
from uvicorn import run

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as users_router

app = FastAPI()


app.include_router(hotels_router)
app.include_router(users_router)


if __name__ == "__main__":
    run("src.main:app", port=8000,  reload=True)
