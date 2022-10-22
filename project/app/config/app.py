import logging
import os

from dotenv import load_dotenv
from functools import lru_cache
from fastapi import Path
from pydantic import BaseSettings
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

    MAIL_TEMPLATE_FOLDER: str = "app/email-templates/build"

    email_configuration = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=os.getenv("MAIL_PORT"),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_TLS=True,
        MAIL_SSL=False,
        TEMPLATE_FOLDER=MAIL_TEMPLATE_FOLDER,
    )


@lru_cache()  # pragma: no cover
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


app_secret: str = os.getenv("APP_SECRET_KEY", None)
app_hash_algorithm: str = os.getenv("APP_HASH_ALGORITHM", None)
app_access_token_expire_minutes: float = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)


settings = Settings()
