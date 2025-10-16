from dataclasses import dataclass
from typing import dataclass_transform, override


@dataclass_transform(
    kw_only_default=True,
    eq_default=False,
)
def to_error[T](cls: type[T]) -> type[T]:
    return dataclass(
        kw_only=True,
        eq=False,
        repr=False,
        match_args=False,
    )(cls)


@to_error
class ApplicationError(Exception):
    pass


@to_error
class EntityAlreadyDeletedError(ApplicationError):
    entity_name: str

    @override
    def __str__(self) -> str:
        return f"Entity {self.entity_name!r} already deleted"
