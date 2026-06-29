import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import run

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.hotels import router as hotels_router
from src.api.auth import router as users_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
from src.api.images import router as image_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    "контекстный менеджер управляющий подключением к Redis"
    await redis_manager.connect()  # при старте приложения
    FastAPICache.init(RedisBackend(redis_manager._redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()  # при остановке/перезапуске приложения


app = FastAPI(lifespan=lifespan)


app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(image_router)


if __name__ == "__main__":
    run("src.main:app", port=8000, reload=True)
