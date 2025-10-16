from abc import abstractmethod
from typing import Protocol

from template_project.application.user.entity import User


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user(self) -> User:
        raise NotImplementedError
