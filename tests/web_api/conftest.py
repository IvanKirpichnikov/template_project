from collections.abc import AsyncIterable
from pathlib import Path

import pytest
from dishka import AsyncContainer

from template_project.web_api.configuration import load_configuration
from tests.web_api.ioc import make_ioc


@pytest.fixture
async def dishka_container() -> AsyncIterable[AsyncContainer]:
    path = Path("config.toml")
    configuration = load_configuration(path)
    ioc = make_ioc(configuration)
    yield ioc
    await ioc.close()
