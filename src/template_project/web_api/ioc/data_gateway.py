from dishka import BaseScope, Provider, Scope, WithParents, provide, provide_all

from template_project.adapters.data_gateways.access_token import DefaultAccessTokenDataGateway
from template_project.adapters.data_gateways.user import DefaultUserDataGateway
from template_project.adapters.unit_of_work import DefaultUnitOfWork


class DataGatewayProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    unit_of_work = provide(WithParents[DefaultUnitOfWork])
    data_gateways = provide_all(
        WithParents[DefaultUserDataGateway],
        WithParents[DefaultAccessTokenDataGateway],
    )
