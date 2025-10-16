from typing import override
from uuid import UUID

from cryptography.fernet import Fernet

from template_project.application.access_token.cryptographer import AccessTokenCryptographer
from template_project.application.access_token.entity import AccessTokenId


type RawAccessToken = str


class FernetAccessTokenCryptographer(AccessTokenCryptographer):
    def __init__(self, fernet: Fernet) -> None:
        self._fernet = fernet

    @override
    def crypto(self, access_token_id: AccessTokenId) -> RawAccessToken:
        return self._fernet.encrypt(
            str(access_token_id).encode("utf-8"),
        ).decode("utf-8")

    @override
    def decrypto(self, raw_access_token: RawAccessToken) -> AccessTokenId:
        return AccessTokenId(
            UUID(
                self._fernet.decrypt(raw_access_token).decode("utf-8"),
            ),
        )
