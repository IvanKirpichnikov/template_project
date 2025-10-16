from typing import override
from template_project.application.common.errors import ApplicationError, to_error


@to_error
class UserWithEmailAlreadyExistsError(ApplicationError):
    email: str

    @override
    def __str__(self) -> str:
        return f"User with the email={self.email!r} already exists"

@to_error
class UserUnauthorizedError(ApplicationError):
    pass
