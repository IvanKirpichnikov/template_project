from dishka import STRICT_VALIDATION, AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from template_project.web_api.configuration import (
    AccessTokenConfiguration,
    Configuration,
    DatabaseConfiguration,
    ServerConfiguration,
)
from template_project.web_api.ioc.connection import ConnectionProvider
from template_project.web_api.ioc.cryptographer import CryptographerProvider
from template_project.web_api.ioc.data_gateway import DataGatewayProvider
from template_project.web_api.ioc.factory import FactoryProvider
from template_project.web_api.ioc.idp import IdPProvider
from template_project.web_api.ioc.interactor import InteractorProvider


def make_ioc(configuration: Configuration) -> AsyncContainer:
    return make_async_container(
        IdPProvider(),
        FactoryProvider(),
        FastapiProvider(),
        ConnectionProvider(),
        InteractorProvider(),
        DataGatewayProvider(),
        CryptographerProvider(),
        validation_settings=STRICT_VALIDATION,
        context={
            ServerConfiguration: configuration.server,
            DatabaseConfiguration: configuration.database,
            AccessTokenConfiguration: configuration.access_token,
        },
    )
