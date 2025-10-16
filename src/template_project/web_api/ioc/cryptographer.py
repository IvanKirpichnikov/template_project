import argon2
from cryptography.fernet import Fernet
from dishka import Provider, Scope, WithParents, provide, provide_all

from template_project.adapters.access_token.cryptographer import FernetAccessTokenCryptographer
from template_project.adapters.password_utils import ArgonPasswordHasher, ArgonPasswordVerifying
from template_project.web_api.configuration import AccessTokenConfiguration


class CryptographerProvider(Provider):
    scope = Scope.APP

    @provide
    def argon_password_hasher(self) -> argon2.PasswordHasher:
        return argon2.PasswordHasher()

    @provide
    def fernet(self, configuration: AccessTokenConfiguration) -> Fernet:
        return Fernet(configuration.crypto_key)

    access_token_cryptographer = provide(WithParents[FernetAccessTokenCryptographer])
    password_utils = provide_all(
        WithParents[ArgonPasswordHasher],
        WithParents[ArgonPasswordVerifying],
    )
