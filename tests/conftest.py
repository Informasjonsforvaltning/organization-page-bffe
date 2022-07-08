"""Conftest module."""
from asyncio import AbstractEventLoop
import datetime
import os
import time
from typing import Any
from unittest.mock import Mock

from dotenv import load_dotenv
import pytest
from pytest_mock import MockFixture
import requests
from requests.exceptions import ConnectionError

from fdk_organization_bff import create_app


load_dotenv()
HOST_PORT = int(os.environ.get("HOST_PORT", "8080"))
MOCKED_DATE = datetime.date(2021, 4, 10)


def is_responsive(url: Any) -> Any:
    """Return true if response from service is 200."""
    url = f"{url}/ready"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            time.sleep(2)  # sleep extra 2 sec
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def docker_service(docker_ip: Any, docker_services: Any) -> Any:
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("fdk-organization-bff", HOST_PORT)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Any) -> Any:
    """Override default location of docker-compose.yml file."""
    return os.path.join(str(pytestconfig.rootdir), "./", "docker-compose.yml")


@pytest.mark.integration
@pytest.fixture(scope="function")
def client(loop: AbstractEventLoop, aiohttp_client: Any) -> Any:
    """Return an aiohttp client for testing."""
    return loop.run_until_complete(
        aiohttp_client(loop.run_until_complete(create_app()))
    )


@pytest.fixture
def mock_datetime(mocker: MockFixture) -> Mock:
    """Mock datetime."""
    mock = mocker.patch("datetime.date")
    mock.today.return_value = MOCKED_DATE
    return mock


@pytest.fixture
def mock_fetch_org_dataset_catalog_scores(mocker: MockFixture) -> Mock:
    """Mock fetch_org_dataset_catalog_scores."""
    mock = mocker.patch(
        "fdk_organization_bff.service.org_catalog_service.fetch_org_dataset_catalog_scores"
    )
    return mock
