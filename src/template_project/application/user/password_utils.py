from abc import abstractmethod
from typing import Protocol

from template_project.application.common.containers import SecretString


class PasswordHasher(Protocol):
    @abstractmethod
    def hash(self, password: SecretString) -> str:
        raise NotImplementedError


class PasswordVerifying(Protocol):
    @abstractmethod
    def verify(
        self,
        verifiable_password: SecretString,
        hashed_password: str,
    ) -> bool:
        raise NotImplementedError
