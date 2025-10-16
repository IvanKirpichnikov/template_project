from typing import override

import argon2
from argon2.exceptions import Argon2Error

from template_project.application.common.containers import SecretString
from template_project.application.user.password_utils import PasswordHasher, PasswordVerifying


class ArgonPasswordHasher(PasswordHasher):
    def __init__(
        self,
        password_hasher: argon2.PasswordHasher,
    ) -> None:
        self._password_hasher = password_hasher

    @override
    def hash(self, password: SecretString) -> str:
        return self._password_hasher.hash(password.get_value())


class ArgonPasswordVerifying(PasswordVerifying):
    def __init__(
        self,
        password_hasher: argon2.PasswordHasher,
    ) -> None:
        self._password_hasher = password_hasher

    @override
    def verify(
        self,
        verifiable_password: SecretString,
        hashed_password: str,
    ) -> bool:
        try:
            return self._password_hasher.verify(hashed_password, verifiable_password.get_value())
        except Argon2Error:
            return False
