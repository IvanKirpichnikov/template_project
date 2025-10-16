import argparse
import asyncio
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Final

import uvicorn
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from template_project.web_api.configuration import load_configuration
from template_project.web_api.ioc.make import make_ioc
from template_project.web_api.routes import healthcheck, user

LOG_CONFIG: Final = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def make_asgi_application(
    ioc: AsyncContainer,
) -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        title="Template project",
        description="Template project API",
        version="1.0.0",
        openapi_url="/openapi.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(user.router)
    app.include_router(healthcheck.router)

    setup_dishka(container=ioc, app=app)

    return app


def _main(
    configuration_path: Path,
) -> None:
    configuration = load_configuration(configuration_path)
    ioc = make_ioc(configuration)
    asgi_application = make_asgi_application(ioc)

    uvicorn.run(
        asgi_application,
        port=configuration.server.port,
        host=configuration.server.host,
        log_config=LOG_CONFIG,
        access_log=configuration.server.access_log,
    )


def main() -> None:
    if sys.platform == "win32":
        from asyncio import WindowsSelectorEventLoopPolicy  # noqa: PLC0415

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("configuration", default=None)

    args = arg_parser.parse_args()
    configuration_path = args.configuration or os.getenv("CONFIGURATION_PATH")

    if configuration_path is None:
        raise RuntimeError(
            "pass the path to the config or specify it in the environment variables `CONFIGURATION_PATH`",
        )

    _main(Path(configuration_path))


if __name__ == "__main__":
    main()
