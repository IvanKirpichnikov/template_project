from abc import abstractmethod
from typing import Protocol

from template_project.application.access_token.entity import AccessToken, AccessTokenId


class AccessTokenDataGateway(Protocol):
    @abstractmethod
    async def load_with_id(self, access_token_id: AccessTokenId) -> AccessToken | None:
        raise NotImplementedError
