from typing import override

from template_project.application.access_token.entity import AccessToken
from template_project.application.access_token.entity_factory import AccessTokenFactory
from template_project.application.user.entity import UserId
from template_project.web_api.configuration import AccessTokenConfiguration


class DefaultAccessTokenFactory(AccessTokenFactory):
    def __init__(self, configuration: AccessTokenConfiguration) -> None:
        self._configuration = configuration

    @override
    def execute(self, user_id: UserId) -> AccessToken:
        return AccessToken.factory(
            user_id=user_id,
            expires_in=self._configuration.expires_in,
        )
