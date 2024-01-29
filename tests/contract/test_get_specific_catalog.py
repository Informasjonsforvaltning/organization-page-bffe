"""Contract test cases for specific organization catalogs."""

import json

import pytest
import requests

from tests import responses


@pytest.mark.contract
@pytest.mark.docker
def test_liland(docker_service: str) -> None:
    """Should return the liland response."""
    url = f"{docker_service}/organizationcatalogs/910258028"
    response = requests.get(url, timeout=30)

    assert response.status_code == 200
    assert response.json() == json.loads(responses.liland)


@pytest.mark.contract
@pytest.mark.docker
def test_response_has_fifteen_minute_cache_headers(docker_service: str) -> None:
    """Should include no-cache headers."""
    url = f"{docker_service}/organizationcatalogs/910258028"
    response = requests.get(url, timeout=30)

    assert response.status_code == 200
    assert (
        response.headers.get("Cache-Control")
        == "no-cache, no-store, max-age=900, must-revalidate"
    )


@pytest.mark.contract
@pytest.mark.docker
def test_not_found(docker_service: str) -> None:
    """Should return 404."""
    url = f"{docker_service}/organizationcatalogs/123"
    response = requests.get(url, timeout=30)

    assert response.status_code == 404


@pytest.mark.contract
@pytest.mark.docker
def test_nap_ramsund(docker_service: str) -> None:
    """Should return the ramsund_nap response."""
    url = f"{docker_service}/organizationcatalogs/910244132?filter=transportportal"
    response = requests.get(url, timeout=30)

    assert response.status_code == 200
    assert response.json() == json.loads(responses.ramsund_nap)


@pytest.mark.contract
@pytest.mark.docker
def test_invalid_filter(docker_service: str) -> None:
    """Should return 400."""
    url = f"{docker_service}/organizationcatalogs/910244132?filter=invalid"
    response = requests.get(url, timeout=30)

    assert response.status_code == 400
