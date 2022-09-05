import logging

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from app.config import database

log = logging.getLogger("uvicorn")


TORTOISE_ORM = {
    "connections": {"default": database.db_url},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=database.db_url,
        modules={"models": ["app.models.user"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=database.db_url,
        modules={"models": ["models.tortoise"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
