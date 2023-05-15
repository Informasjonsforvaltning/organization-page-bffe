"""Integration test cases for organization categories."""
from aiohttp.test_utils import TestClient
import pytest


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.asyncio
async def test_state_categories(client: TestClient, docker_service: str) -> None:
    """Should return the state categories response without empty orgs."""
    response = await client.get("/organizationcategories/state?includeEmpty=false")
    response_json = await response.json()

    assert response.status == 200
    assert len(response_json["categories"]) == 19
    assert response_json["categories"][0]["category"]["id"] == "912660680"
    assert len(response_json["categories"][0]["organizations"]) == 1


@pytest.mark.integration
@pytest.mark.docker
@pytest.mark.asyncio
async def test_state_categories_include_empty(
    client: TestClient, docker_service: str
) -> None:
    """Should return the state categories response with empty orgs."""
    response = await client.get("/organizationcategories/state?includeEmpty=true")
    response_json = await response.json()

    assert response.status == 200
    assert len(response_json["categories"]) == 19
    assert response_json["categories"][0]["category"]["id"] == "912660680"
    assert len(response_json["categories"][0]["organizations"]) == 20
