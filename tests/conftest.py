import time
import pytest
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError

from src.utils import ServiceKey
from tests.test_data import org_brreg, org_digdir, concept_es_response, info_es_response_size_1_total_7, \
    org_politi


@pytest.fixture(scope="session")
def wait_for_ready():
    wait_for_mock_server()
    timeout = time.time() + 20
    try:
        while True:
            response = requests.get("http://localhost:8000/ready")
            if response.status_code == 200:
                break
            if time.time() > timeout:
                pytest.fail(
                    'Test function setup: timed out while waiting for organization-bff, last response '
                    'was {0}'.format(response.status_code))
            time.sleep(1)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test function setup: could not contact fdk-organization-bff')
    yield


def wait_for_mock_server():
    timeout = time.time() + 10
    while True:
        try:
            response = requests.get("http://localhost:8080/ready")
            if response.status_code == 200:
                break
            if time.time() > timeout:
                pytest.fail(
                    'Test function setup: timed out while waiting for organization-bff, last response '
                    'was {0}'.format(response.status_code))
            time.sleep(1)
        except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
            continue
    return


def get_xhttp_mock(status_code, service_key=None, organizations=None, json=None, text=None):
    class MockResponse:
        def __init__(self, status):
            if service_key == ServiceKey.ORGANIZATIONS:
                self.json_data = [org_brreg, org_digdir, org_politi]
            elif service_key == ServiceKey.CONCEPTS:
                self.json_data = concept_es_response
            elif service_key == ServiceKey.DATASETS:
                self.json_data = {"results": {"bindings": []}}
            elif service_key == ServiceKey.DATA_SERVICES:
                self.json_data = {"results": {"bindings": []}}
            elif service_key == ServiceKey.INFO_MODELS:
                self.json_data = info_es_response_size_1_total_7
            elif json:
                self.json_data = json
            elif text:
                self.text = text
            else:
                self.json_data = {}
            self.status_code = status

        def json(self):
            return self.json_data

        def raise_for_status(self):
            pass

    return MockResponse(status_code)


@pytest.fixture
def mock_get_xhttp_organizations(mocker):
    mock_values = get_xhttp_mock(status_code=200, service_key=ServiceKey.ORGANIZATIONS)
    return mocker.patch('httpx.AsyncClient.get',
                        return_value=mock_values
                        )


@pytest.fixture
def mock_get_xhttp_concepts(mocker):
    mock_values = get_xhttp_mock(status_code=200, service_key=ServiceKey.CONCEPTS)
    return mocker.patch('httpx.AsyncClient.get',
                        return_value=mock_values
                        )


@pytest.fixture
def mock_get_xhttp_dataservices(mocker):
    mock_values = get_xhttp_mock(status_code=200, service_key=ServiceKey.DATA_SERVICES)
    return mocker.patch('httpx.AsyncClient.get',
                        return_value=mock_values
                        )


@pytest.fixture
def mock_get_xhttp_datasets(mocker):
    mock_values = get_xhttp_mock(status_code=200, service_key=ServiceKey.DATASETS)
    return mocker.patch('httpx.AsyncClient.get',
                        return_value=mock_values
                        )


@pytest.fixture
def mock_get_xhttp_informationmodels(mocker):
    mock_values = get_xhttp_mock(status_code=200, service_key=ServiceKey.INFO_MODELS)
    return mocker.patch('httpx.AsyncClient.get',
                        return_value=mock_values
                        )


@pytest.fixture
def mock_get_xhttp_informationmodels_empty(mocker):
    mock_values = get_xhttp_mock(status_code=200, service_key="empty")
    return mocker.patch('httpx.AsyncClient.get',
                        return_value=mock_values
                        )
