from abc import abstractmethod

from fastapi import Request

from template_project.application.access_token.cryptographer import AccessTokenCryptographer
from template_project.application.access_token.data_gateway import AccessTokenDataGateway
from template_project.application.access_token.entity import AccessTokenId
from template_project.application.access_token.errors import AccessTokenExpiredError
from template_project.application.common.identity_provider import IdentityProvider
from template_project.application.user.data_gateway import UserDataGateway
from template_project.application.user.entity import User
from template_project.application.user.errors import UserUnauthorizedError


TOKEN_TYPE = "Bearer"
BEARER_SECTIONS = 2
AUTH_HEADER = "Authorization"


class WebApiIdentityProvider(IdentityProvider):
    def __init__(
        self,
        request: Request,
        user_data_gateway: UserDataGateway,
        access_token_data_gateway: AccessTokenDataGateway,
        access_token_cryptographer: AccessTokenCryptographer,
    ) -> None:
        self._request = request

        self._user_data_gateway = user_data_gateway
        self._access_token_data_gateway = access_token_data_gateway
        self._access_token_cryptographer = access_token_cryptographer

    @abstractmethod
    async def get_current_user(self) -> User:
        auth_tokn = self._request.headers[AUTH_HEADER]

        access_token_id = self._parse_token(auth_tokn)
        if access_token_id is None:
            raise UserUnauthorizedError

        access_token = await self._access_token_data_gateway.load_with_id(access_token_id)
        if access_token is None:
            raise UserUnauthorizedError

        try:
            access_token.ensure_expired()
        except AccessTokenExpiredError as error:
            raise UserUnauthorizedError from error

        user = await self._user_data_gateway.load_with_id(access_token.user_id)

        if user is None:
            raise UserUnauthorizedError

        return user

    def _parse_token(self, token: str) -> AccessTokenId | None:
        authorization_header = self._request.headers.get(AUTH_HEADER)

        if authorization_header is None:
            return None

        sections = authorization_header.split(" ")
        if len(sections) != BEARER_SECTIONS:
            return None

        token_type, token = sections

        if token_type != TOKEN_TYPE:
            return None

        return self._access_token_cryptographer.decrypto(token)
