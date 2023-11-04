import logging

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class DbSettings(BaseSettings):
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_PORT: str
    MONGO_HOST: str
    DB_NAME: str

    def get_url(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}"


class APISettings(BaseSettings):
    APP_PORT: int
    APP_HOST: str


class LogSettings(BaseSettings):
    LEVEL: int = logging.DEBUG


db = DbSettings()
log = LogSettings()
api = APISettings()
