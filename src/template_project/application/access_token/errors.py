from typing import override

from template_project.application.access_token.entity import AccessTokenId
from template_project.application.common.errors import ApplicationError, to_error


@to_error
class AccessTokenExpiredError(ApplicationError):
    id_: AccessTokenId

    @override
    def __str__(self) -> str:
        return f"Access token id={self.id_!r} expried"
