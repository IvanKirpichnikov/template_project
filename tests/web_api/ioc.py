from collections.abc import Callable
from inspect import Parameter
from typing import Final

from dishka import STRICT_VALIDATION, AsyncContainer, BaseScope, Provider, Scope, make_async_container, provide
from dishka.integrations.base import wrap_injection
from dishka.integrations.fastapi import FastapiProvider
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from template_project.web_api.configuration import (
    AccessTokenConfiguration,
    Configuration,
    DatabaseConfiguration,
    ServerConfiguration,
)
from template_project.web_api.ioc.connection import ConnectionProvider
from template_project.web_api.ioc.cryptographer import CryptographerProvider
from template_project.web_api.ioc.data_gateway import DataGatewayProvider
from template_project.web_api.ioc.factory import FactoryProvider
from template_project.web_api.ioc.idp import IdPProvider
from template_project.web_api.ioc.interactor import InteractorProvider


class DatabaseClearer:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def clear(self) -> None:
        await self._session.execute(
            text("""
                DO $$
                DECLARE
                    tb text;
                BEGIN
                    FOR tb IN (
                        SELECT tablename
                        FROM pg_catalog.pg_tables
                        WHERE schemaname = 'public'
                        AND tablename != 'alembic_version'
                    )
                    LOOP
                        EXECUTE 'TRUNCATE TABLE ' || tb || ' CASCADE';
                    END LOOP;
                END $$;
            """),
        )


class TestProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    database_clearer = provide(DatabaseClearer)

    @provide
    def http_client(self) -> AsyncClient:
        return AsyncClient(base_url="http://web_api:8080")


def make_ioc(configuration: Configuration) -> AsyncContainer:
    return make_async_container(
        IdPProvider(),
        FactoryProvider(),
        FastapiProvider(),
        ConnectionProvider(),
        InteractorProvider(),
        DataGatewayProvider(),
        CryptographerProvider(),
        TestProvider(),
        validation_settings=STRICT_VALIDATION,
        context={
            ServerConfiguration: configuration.server,
            DatabaseConfiguration: configuration.database,
            AccessTokenConfiguration: configuration.access_token,
        },
    )


CONTAINER_PARAM: Final = "dishka_container"


def inject[ReturnT, **FuncParams](func: Callable[FuncParams, ReturnT]) -> Callable[FuncParams, ReturnT]:
    return wrap_injection(
        func=func,
        is_async=True,
        manage_scope=True,
        container_getter=lambda args, kwargs: kwargs[CONTAINER_PARAM],
        additional_params=[
            Parameter(
                name=CONTAINER_PARAM,
                annotation=AsyncContainer,
                kind=Parameter.KEYWORD_ONLY,
            ),
        ],
    )
