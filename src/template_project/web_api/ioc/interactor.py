from dishka import BaseScope, Provider, Scope, provide_all

from template_project.application.user.interactors.sign_up import UserSignUpInteractor


class InteractorProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    interactors = provide_all(
        UserSignUpInteractor,
    )
