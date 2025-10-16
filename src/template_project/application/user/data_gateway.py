from abc import abstractmethod
from typing import Protocol

from template_project.application.user.entity import User, UserId


class UserDataGateway(Protocol):
    @abstractmethod
    async def load_with_id(self, id_: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        raise NotImplementedError
