from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(
    frozen_default=True,
    eq_default=False,
    kw_only_default=True,
)
def to_interactor[_InteractorClsT](interactor_cls: type[_InteractorClsT]) -> type[_InteractorClsT]:
    return dataclass(
        kw_only=True,
        eq=False,
        repr=False,
        frozen=True,
        match_args=False,
        slots=True,
    )(interactor_cls)