from typing import override
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from template_project.adapters.data_gateways.tables import user_table
from template_project.application.user.data_gateway import UserDataGateway
from template_project.application.user.entity import User, UserId


class DefaultUserDataGateway(UserDataGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def load_with_id(self, id_: UserId) -> User | None:
        statement = select(User).where(user_table.c.id==id_)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    @override
    async def exists_by_email(self, email: str) -> bool:
        statement = select(exists(select(user_table).where(user_table.c.email == email)))
        result = await self._session.execute(statement)
        result_fetchone = result.fetchone()
        if result_fetchone is None:
            return False
        return result_fetchone[0]
