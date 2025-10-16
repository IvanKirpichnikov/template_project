from adaptix.conversion import get_converter

from template_project.application.common.data_structure import to_data_structure
from template_project.application.common.identity_provider import IdentityProvider
from template_project.application.common.interactor import to_interactor
from template_project.application.user.entity import User, UserId


@to_data_structure
class GetMeResponse:
    id: UserId
    email: str


response_converter = get_converter(User, GetMeResponse)


@to_interactor
class GetMeInteractor:
    identity_provider: IdentityProvider

    async def execute(self) -> GetMeResponse:
        current_user = await self.identity_provider.get_current_user()
        return response_converter(current_user)
