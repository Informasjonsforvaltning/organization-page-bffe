"""Conftest module."""
from asyncio import AbstractEventLoop
import os
import time
from typing import Any

from dotenv import load_dotenv
import pytest
import requests
from requests.exceptions import ConnectionError

from fdk_organization_bff import create_app

load_dotenv()
HOST_PORT = int(os.environ.get("HOST_PORT", "8080"))


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
