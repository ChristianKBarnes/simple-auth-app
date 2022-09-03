import logging
import os

from dotenv import load_dotenv
from functools import lru_cache
from pydantic import AnyUrl, BaseSettings

from app.config import database

log = logging.getLogger("uvicorn")
load_dotenv()


class Settings(BaseSettings):
    environment: str = os.getenv("APP_ENVIRONMENT", "development")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = database.db_url


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
