from typing import Any, override

from sqlalchemy.ext.asyncio import AsyncSession

from template_project.application.common.unit_of_work import UnitOfWork


class DefaultUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    def add(self, *entities: Any) -> None:
        self._session.add_all(entities)

    @override
    async def commit(self) -> None:
        await self._session.commit()
