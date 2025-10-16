from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from template_project.web_api.configuration import DatabaseConfiguration


class ConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    async def make_engine(self, configuration: DatabaseConfiguration) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(configuration.url.get_value())
        yield engine
        await engine.dispose()

    @provide()
    async def make_connection(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        session = AsyncSession(
            bind=engine,
            expire_on_commit=True,
        )
        async with session:
            yield session
