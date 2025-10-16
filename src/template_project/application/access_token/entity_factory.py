from abc import abstractmethod
from typing import Protocol

from template_project.application.access_token.entity import AccessToken
from template_project.application.user.entity import UserId


class AccessTokenFactory(Protocol):
    @abstractmethod
    def execute(self, user_id: UserId) -> AccessToken:
        raise NotImplementedError
