from abc import abstractmethod
from typing import Protocol

from template_project.application.access_token.entity import AccessTokenId


type RawAccessToken = str


class AccessTokenCryptographer(Protocol):
    @abstractmethod
    def crypto(self, access_token_id: AccessTokenId) -> RawAccessToken:
        raise NotImplementedError

    @abstractmethod
    def decrypto(self, raw_access_token: RawAccessToken) -> AccessTokenId:
        raise NotImplementedError
