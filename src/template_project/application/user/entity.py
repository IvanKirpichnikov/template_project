from datetime import UTC, datetime
from typing import NewType, Self
from uuid import UUID

from uuid_utils.compat import uuid7

from template_project.application.common.entity import Entity, to_entity

UserId = NewType("UserId", UUID)


@to_entity
class User(Entity[UserId]):
    email: str
    hashed_password: str

    @classmethod
    def factory(
        cls,
        email: str,
        hashed_password: str,
    ) -> Self:
        return cls(
            id=UserId(uuid7()),
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.now(tz=UTC),
        )
