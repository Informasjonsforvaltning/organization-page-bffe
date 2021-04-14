"""Contract test cases for specific organization catalogs."""
import json

import pytest
import requests

from tests import responses


@pytest.mark.contract
@pytest.mark.docker
def test_fiskeri(docker_service: str) -> None:
    """Should return the fiskeri response."""
    url = f"{docker_service}/organizationcatalog/971203420"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == json.loads(responses.fiskeri)


@pytest.mark.contract
@pytest.mark.docker
def test_not_found(docker_service: str) -> None:
    """Should return 404."""
    url = f"{docker_service}/organizationcatalog/123"
    response = requests.get(url)

    assert response.status_code == 404


@pytest.mark.contract
@pytest.mark.docker
def test_nap_ramsund(docker_service: str) -> None:
    """Should return the ramsund_nap response."""
    url = f"{docker_service}/organizationcatalog/910244132?filter=transportportal"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == json.loads(responses.ramsund_nap)


@pytest.mark.contract
@pytest.mark.docker
def test_invalid_filter(docker_service: str) -> None:
    """Should return 400."""
    url = f"{docker_service}/organizationcatalog/910244132?filter=invalid"
    response = requests.get(url)

    assert response.status_code == 400
