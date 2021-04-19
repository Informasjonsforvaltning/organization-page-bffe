"""Contract test cases for cases for all organization catalogs."""
import json

import pytest
import requests

from tests import responses


@pytest.mark.contract
@pytest.mark.docker
def test_all_catalogs(docker_service: str) -> None:
    """Should return the all_catalogs response."""
    url = f"{docker_service}/organizationcatalogs"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == json.loads(responses.all_catalogs)


@pytest.mark.contract
@pytest.mark.docker
def test_all_nap_catalogs(docker_service: str) -> None:
    """Should return the all_nap response."""
    url = f"{docker_service}/organizationcatalogs?filter=transportportal"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == json.loads(responses.all_nap)


@pytest.mark.contract
@pytest.mark.docker
def test_invalid_filter(docker_service: str) -> None:
    """Should return 400."""
    url = f"{docker_service}/organizationcatalogs?filter=invalid"
    response = requests.get(url)

    assert response.status_code == 400
