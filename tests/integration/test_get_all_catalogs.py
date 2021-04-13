"""Integration test cases for all organization catalogs."""
import json

from aiohttp.test_utils import TestClient
import pytest

from tests import responses


@pytest.mark.integration
@pytest.mark.docker
async def test_all(client: TestClient, docker_service: str) -> None:
    """Should return the all_catalogs response."""
    response = await client.get("/organizationcatalog")
    response_json = await response.json()

    assert response.status == 200
    assert response_json == json.loads(responses.all_catalogs)
