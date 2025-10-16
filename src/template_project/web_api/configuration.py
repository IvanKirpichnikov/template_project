from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from tomllib import loads
from typing import dataclass_transform
from adaptix import P, Retort, loader

from template_project.application.common.containers import SecretString


@dataclass_transform(frozen_default=True)
def to_configuration[ClsT](cls: type[ClsT]) -> type[ClsT]:
    return dataclass(frozen=True, slots=True, repr=False)(cls)


@to_configuration
class DatabaseConfiguration:
    url: SecretString


@to_configuration
class AccessTokenConfiguration:
    crypto_key: str
    expires_in: timedelta


@to_configuration
class ServerConfiguration:
    host: str
    port: int
    access_log: bool


@to_configuration
class Configuration:
    server: ServerConfiguration
    database: DatabaseConfiguration
    access_token: AccessTokenConfiguration


retort = Retort(
    recipe=[
        loader(SecretString, SecretString),
        loader(P[AccessTokenConfiguration].expires_in, lambda value: timedelta(seconds=value)),
    ],
)


def load_configuration(path: Path) -> Configuration:
    with path.open("r", encoding="utf-8") as config:
        data = loads(config.read())

    return retort.load(data, Configuration)
