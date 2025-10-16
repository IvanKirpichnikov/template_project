from template_project.application.access_token.cryptographer import AccessTokenCryptographer
from template_project.application.access_token.entity_factory import AccessTokenFactory
from template_project.application.common.containers import SecretString
from template_project.application.common.data_structure import to_data_structure
from template_project.application.common.interactor import to_interactor
from template_project.application.common.unit_of_work import UnitOfWork
from template_project.application.user.data_gateway import UserDataGateway
from template_project.application.user.entity import User
from template_project.application.user.errors import UserWithEmailAlreadyExistsError
from template_project.application.user.password_utils import PasswordHasher


@to_data_structure
class UserSignUpResponse:
    access_token: str


@to_interactor
class UserSignUpInteractor:
    unit_of_work: UnitOfWork
    password_hasher: PasswordHasher
    user_data_gateway: UserDataGateway
    access_token_factory: AccessTokenFactory
    access_token_cryptographer: AccessTokenCryptographer

    async def execute(
        self,
        email: str,
        password: SecretString,
    ) -> UserSignUpResponse:
        exists_by_email = await self.user_data_gateway.exists_by_email(email)
        if exists_by_email:
            raise UserWithEmailAlreadyExistsError(email=email)

        hashed_password = self.password_hasher.hash(password)

        user = User.factory(
            email=email,
            hashed_password=hashed_password,
        )
        access_token = self.access_token_factory.execute(user.id)
        crypted_access_token = self.access_token_cryptographer.crypto(access_token)

        response = UserSignUpResponse(access_token=crypted_access_token)

        self.unit_of_work.add(user, access_token)
        await self.unit_of_work.commit()

        return response
