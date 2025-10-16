from dishka import FromDishka
from httpx import AsyncClient

from tests.web_api.ioc import inject


@inject
async def test_healthcheck(
    http_client: FromDishka[AsyncClient],
) -> None:
    response = await http_client.get("/healthcheck")
    response_json = response.json()

    assert response_json["ok"]
