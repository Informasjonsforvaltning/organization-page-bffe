"""Integration test cases for specific organizations."""
import json
from unittest.mock import Mock

from aiohttp.test_utils import TestClient
from asynctest import CoroutineMock
import pytest

from tests import responses


@pytest.mark.integration
@pytest.mark.docker
async def test_ramsund(
    client: TestClient, docker_service: str, mock_datetime: Mock
) -> None:
    """Should return the ramsund response."""
    response = await client.get("/organizationcatalogs/910244132")
    response_json = await response.json()

    assert response.status == 200
    assert response_json == json.loads(responses.ramsund)


@pytest.mark.integration
@pytest.mark.docker
async def test_liland(client: TestClient, docker_service: str) -> None:
    """Should return the liland response."""
    response = await client.get("/organizationcatalogs/910258028")
    response_json = await response.json()

    assert response.status == 200
    assert response_json == json.loads(responses.liland)


@pytest.mark.integration
@pytest.mark.docker
async def test_not_found(client: TestClient, docker_service: str) -> None:
    """Should return 404."""
    response = await client.get("/organizationcatalogs/123")

    assert response.status == 404


@pytest.mark.integration
@pytest.mark.docker
async def test_nap_ramsund(client: TestClient, docker_service: str) -> None:
    """Should return the ramsund_nap response."""
    response = await client.get(
        "/organizationcatalogs/910244132?filter=transportportal"
    )
    response_json = await response.json()

    assert response.status == 200
    assert response_json == json.loads(responses.ramsund_nap)


@pytest.mark.integration
@pytest.mark.docker
async def test_invalid_filter(client: TestClient, docker_service: str) -> None:
    """Should return 400."""
    response = await client.get("/organizationcatalogs/910244132?filter=invalid")

    assert response.status == 400


@pytest.mark.integration
@pytest.mark.docker
async def test_ntnu_remote_services_fail(
    client: TestClient, docker_service: str
) -> None:
    """Should return 200."""
    response = await client.get("/organizationcatalogs/974767880")
    response_json = await response.json()

    assert response.status == 200
    assert response_json == json.loads(responses.ntnu)


@pytest.mark.integration
@pytest.mark.docker
async def test_get_organization_catalog_with_failing_quality(
    client: TestClient,
    docker_service: str,
    mock_fetch_org_dataset_catalog_scores: Mock,
    mock_datetime: Mock,
) -> None:
    """Mock closed session and get organization catalogs."""
    mock_fetch_org_dataset_catalog_scores.return_value.__aenter__.return_value = (
        CoroutineMock(side_effect=True)
    )

    """Should return the ramsund response."""
    response = await client.get("/organizationcatalogs/910244132")
    response_json = await response.json()

    assert response.status == 200
    assert response_json == json.loads(responses.ramsund_with_no_quality)
