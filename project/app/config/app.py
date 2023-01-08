import logging
import os

from dotenv import load_dotenv
from functools import lru_cache
from pydantic import BaseSettings, DirectoryPath
from fastapi_mail import ConnectionConfig

from app.config import database

log = logging.getLogger("uvicorn")
load_dotenv()


class Settings(BaseSettings):
    app_secret: str = os.getenv("APP_SECRET_KEY", None)
    app_hash_algorithm: str = os.getenv("APP_HASH_ALGORITHM", None)
    app_access_token_expire_minutes: float = os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES", 30
    )
    app_name: str = os.getenv("APP_NAME", "Fastapi")
    environment: str = os.getenv("APP_ENVIRONMENT", "development")
    testing: bool = os.getenv("TESTING", 0)
    database_url = database.db_url

    static_directory: DirectoryPath = os.getenv("STATIC_DIRECTORY")

    email_configuration = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=os.getenv("MAIL_PORT"),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        TEMPLATE_FOLDER=os.getenv("MAIL_TEMPLATE_FOLDELR"),
        MAIL_TLS=True,
        MAIL_SSL=False,
    )


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


app_secret: str = os.getenv("APP_SECRET_KEY", None)
app_hash_algorithm: str = os.getenv("APP_HASH_ALGORITHM", 'HS256')
app_access_token_expire_minutes: float = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)


settings = get_settings()
