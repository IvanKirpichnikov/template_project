from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel, SecretStr

from template_project.application.common.containers import SecretString
from template_project.application.user.interactors.sign_up import UserSignUpInteractor


router = APIRouter(route_class=DishkaRoute)


class UserSignUpRequest(BaseModel):
    email: str
    password: SecretStr


class UserSignUpResponse(BaseModel):
    access_token: str


@router.post("/user/sign_up")
async def sign_up(
    request: UserSignUpRequest,
    interactor: FromDishka[UserSignUpInteractor],
) -> UserSignUpResponse:
    response_interactor = await interactor.execute(
        email=request.email,
        password=SecretString(request.password.get_secret_value())
    )
    return UserSignUpResponse(
        access_token=response_interactor.access_token,
    )
