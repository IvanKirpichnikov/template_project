from dishka import BaseScope, Provider, Scope, provide

from template_project.web_api.identity_provider import WebApiIdentityProvider


class IdPProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    web_api = provide(WebApiIdentityProvider)
