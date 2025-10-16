from datetime import UTC, datetime, timedelta
from typing import NewType, Self
from uuid import UUID

from uuid_utils.compat import uuid7

from template_project.application.access_token.errors import AccessTokenExpiredError
from template_project.application.common.entity import Entity, to_entity
from template_project.application.user.entity import UserId

AccessTokenId = NewType("AccessTokenId", UUID)

@to_entity
class AccessToken(Entity[AccessTokenId]):
    user_id: UserId
    revoked: bool
    expires_in: datetime

    @classmethod
    def factory(
        cls,
        user_id: UserId,
        expires_in: timedelta,
    ) -> Self:
        current_date_time = datetime.now(tz=UTC)

        return cls(
            id=AccessTokenId(uuid7()),
            created_at=current_date_time,
            user_id=user_id,
            expires_in=current_date_time + expires_in,
            revoked=False,
        )


    def ensure_expired(self) -> None:
        if self.expired_predicate():
            raise AccessTokenExpiredError(id_=self.id)

    def expired_predicate(self) -> bool:
        return (
            (self.expires_in < datetime.now(tz=UTC))
            or self.revoked
            or self.deleted_at is not None
        )

    def revoke(self) -> None:
        self.revoked = True
        self.deleted_at = datetime.now(tz=UTC)
