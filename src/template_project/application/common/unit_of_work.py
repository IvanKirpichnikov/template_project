from abc import abstractmethod
from typing import Any, Protocol


class UnitOfWork(Protocol):
    @abstractmethod
    def add(self, *entities: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
