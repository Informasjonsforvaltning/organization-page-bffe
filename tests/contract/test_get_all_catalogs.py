"""Contract test cases for cases for all organization catalogs."""
import json

import pytest
import requests

from tests import responses


@pytest.mark.contract
@pytest.mark.docker
def test_ramsund(docker_service: str) -> None:
    """Should return the all_catalogs response."""
    url = f"{docker_service}/organizationcatalog"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == json.loads(responses.all_catalogs)
