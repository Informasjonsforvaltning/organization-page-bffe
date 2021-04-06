"""Contract test cases for ping & ready."""
import pytest
import requests


@pytest.mark.contract
@pytest.mark.docker
def test_ping(docker_service: str) -> None:
    """Should return OK."""
    url = f"{docker_service}/ping"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.text == "OK"


@pytest.mark.contract
@pytest.mark.docker
def test_ready(docker_service: str) -> None:
    """Should return OK."""
    url = f"{docker_service}/ready"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.text == "OK"
