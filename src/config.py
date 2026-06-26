from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def BROCKER_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"  # строка в формате redis://:password@hostname:port/db_number

    @property
    def DB_URL(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()
