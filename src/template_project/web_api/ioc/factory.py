from dishka import Provider, Scope, WithParents, provide_all

from template_project.adapters.access_token.factory import DefaultAccessTokenFactory


class FactoryProvider(Provider):
    scope = Scope.APP

    provides = provide_all(
        WithParents[DefaultAccessTokenFactory],
    )
