from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(route_class=DishkaRoute)


class HealthcheckResponse(BaseModel):
    ok: bool


@router.get("/healthcheck")
async def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse(ok=True)
