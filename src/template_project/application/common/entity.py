from collections.abc import Hashable
from dataclasses import dataclass
from datetime import datetime
from typing import dataclass_transform, override
from uuid import UUID

from template_project.application.common.errors import EntityAlreadyDeletedError


@dataclass_transform(kw_only_default=True)
def to_entity[_EntityCLsT](entity_cls: type[_EntityCLsT]) -> type[_EntityCLsT]:
    return dataclass(kw_only=True)(entity_cls)


@to_entity
class Entity[_EntityId: UUID](Hashable):
    id: _EntityId
    created_at: datetime
    deleted_at: datetime | None = None

    def ensure_not_deleted(self) -> None:
        if self.deleted_at is not None:
            raise EntityAlreadyDeletedError(entity_name=self.__class__.__name__)

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Entity):
            return self.id == other.id
        return NotImplemented

    @override
    def __hash__(self) -> int:
        return hash(self.id)
