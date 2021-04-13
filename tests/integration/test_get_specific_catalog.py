"""Integration test cases for specific organizations."""
import json
from unittest.mock import Mock

from aiohttp.test_utils import TestClient
import pytest

from tests import responses


@pytest.mark.integration
@pytest.mark.docker
async def test_ramsund(
    client: TestClient, docker_service: str, mock_datetime: Mock
) -> None:
    """Should return the ramsund response."""
    response = await client.get("/organizationcatalog/910244132")
    response_json = await response.json()

    assert response.status == 200
    assert response_json == json.loads(responses.ramsund)


@pytest.mark.integration
@pytest.mark.docker
async def test_fiskeri(client: TestClient, docker_service: str) -> None:
    """Should return the fiskeri response."""
    response = await client.get("/organizationcatalog/971203420")
    response_json = await response.json()

    assert response.status == 200
    assert response_json == json.loads(responses.fiskeri)


@pytest.mark.integration
@pytest.mark.docker
async def test_not_found(client: TestClient, docker_service: str) -> None:
    """Should return 404."""
    response = await client.get("/organizationcatalog/123")

    assert response.status == 404
