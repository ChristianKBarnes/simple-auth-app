import logging
import os

from dotenv import load_dotenv
from functools import lru_cache
from pydantic import BaseSettings

from app.config import database

log = logging.getLogger("uvicorn")
load_dotenv()


class Settings(BaseSettings):
    environment: str = os.getenv("APP_ENVIRONMENT", "development")
    testing: bool = os.getenv("TESTING", 0)
    database_url = database.db_url


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


app_secret: str = os.getenv("APP_SECRET_KEY", None)
app_hash_algorithm: str = os.getenv("APP_HASH_ALGORITHM", None)
app_access_token_expire_minutes: float = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
