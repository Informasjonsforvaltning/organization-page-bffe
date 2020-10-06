import pytest
from httpcore import ConnectError
from src.service_requests import ServiceKey, get_organizations_from_catalog, get_datasets, get_dataservices, \
    get_informationmodels, get_concepts
from src.utils import FetchFromServiceException

get_request = "httpx.AsyncClient.get"

service_urls = {
    ServiceKey.ORGANIZATIONS: "http://localhost:8080/organizations",
    ServiceKey.INFO_MODELS: "http://localhost:8080/informationmodels",
    ServiceKey.DATA_SERVICES: "http://localhost:8080/apis",
    ServiceKey.DATASETS: "http://localhost:8080/datasets",
    ServiceKey.CONCEPTS: "http://localhost:8080/concepts"

}


@pytest.mark.unit
def test_get_organizations(event_loop, mock_get_xhttp_organizations):
    event_loop.run_until_complete(get_organizations_from_catalog())
    mock_get_xhttp_organizations.assert_called_once_with(url="http://localhost:8080/organizations",
                                                         headers={"Accept": "application/json"},
                                                         timeout=5)


@pytest.mark.unit
def test_get_organizations_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_organizations_from_catalog())


@pytest.mark.unit
def test_get_concepts_should_get_all_concepts_by_org_path(event_loop, mock_get_xhttp_concepts):
    event_loop.run_until_complete(get_concepts())
    mock_get_xhttp_concepts.assert_called_once_with(url="http://localhost:8080/concepts",
                                                    params={'aggregations': 'orgPath', 'size': '0'}, timeout=5)


@pytest.mark.unit
def test_get_concepts_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_organizations_from_catalog())


@pytest.mark.unit
def test_get_datasets_should_send_sparql_query(event_loop, mock_get_xhttp_datasets):
    event_loop.run_until_complete(get_datasets())
    assert mock_get_xhttp_datasets.call_args.kwargs['url'] == "http://localhost:8080/sparql"
    assert mock_get_xhttp_datasets.call_args.kwargs['headers'] == {
        "accept": "application/json"
    }


@pytest.mark.unit
def test_get_datasets_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_datasets())


@pytest.mark.unit
def test_get_dataservices_should_get_all_dataservices(event_loop, mock_get_xhttp_dataservices):
    event_loop.run_until_complete(get_dataservices())
    assert mock_get_xhttp_dataservices.call_args.kwargs['url'] == "http://localhost:8080/sparql"
    assert mock_get_xhttp_dataservices.call_args.kwargs['headers'] == {
        "accept": "application/json"
    }


@pytest.mark.unit
def test_get_dataservices_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_dataservices())


@pytest.mark.unit
def test_get_informationmodels_should_get_all_models_with_orgapth(event_loop, mock_get_xhttp_informationmodels):
    event_loop.run_until_complete(get_informationmodels())
    mock_get_xhttp_informationmodels.assert_called_once_with(url="http://localhost:8080/informationmodels",
                                                             params={'aggregations': 'orgPath', 'size': 0}, timeout=5)


@pytest.mark.unit
def test_get_informationmodels_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_informationmodels())


class HttpResponseMock:
    def __init__(self, status):
        self.status_code = status
        self.request = {}
