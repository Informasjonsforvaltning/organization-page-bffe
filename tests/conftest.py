import time

import pytest
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError


@pytest.fixture(scope="function")
def wait_for_datasets_ready():
    timeout = time.time() + 90
    try:
        while True:
            response = requests.get("http://localhost:8000/ready")
            if response.json() == 200:
                break
            if time.time() > timeout:
                pytest.fail(
                    'Test function setup: timed out while waiting for organization-bff, last response '
                    'was {0}'.format(response.status_code))
            time.sleep(1)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test function setup: could not contact fdk-organization-bff')
    yield
