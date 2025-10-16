from dishka import Provider, Scope, provide_all

from template_project.adapters.access_token.factory import DefaultAccessTokenFactory


class FactoryProvider(Provider):
    scope = Scope.APP

    factories = provide_all(
        DefaultAccessTokenFactory,
    )
