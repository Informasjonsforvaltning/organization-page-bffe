import pytest
from httpcore import ConnectError
from src.service_requests import ServiceKey, get_organizations_from_catalog, get_datasets, get_dataservices, \
    get_informationmodels
from src.utils import FetchFromServiceException

get_request = "httpx.AsyncClient.get"

service_urls = {
    ServiceKey.ORGANIZATIONS: "http://localhost:8080/organizations",
    ServiceKey.INFO_MODELS: "http://localhost:8080/informationmodels",
    ServiceKey.DATA_SERVICES: "http://localhost:8080/apis",
    ServiceKey.DATA_SETS: "http://localhost:8080/datasets",
    ServiceKey.CONCEPTS: "http://localhost:8080/concepts"

}


@pytest.mark.unit
def test_get_organizations(event_loop, mock_get_xhttp_organizations):
    #event_loop.run_until_complete(get_organizations_from_catalog())
    #mock_get_xhttp_organizations.assert_called_once_with(url="http://localhost:8080/organizations",
    #                                                     headers={"Accept": "application/json"},
    #                                                     timeout=5)

    pytest.xfail()

@pytest.mark.unit
def test_get_organizations_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_organizations_from_catalog())


@pytest.mark.unit
def test_get_concepts_should_get_all_concepts(event_loop, mocker):
    pass


@pytest.mark.unit
def test_get_concepts_should_throw_error(event_loop, mocker):
    pass


@pytest.mark.unit
def test_get_datasets_should_return_parsed_table(event_loop, mocker):
    pass


@pytest.mark.unit
def test_get_datasets_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_datasets())


@pytest.mark.unit
def test_get_dataservices_should_get_all_dataservices(event_loop, mocker):
    pass


@pytest.mark.unit
def test_get_dataservices_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_dataservices())


@pytest.mark.unit
def test_get_informationmodels_should_get_all_models(event_loop, mocker):
    pass


@pytest.mark.unit
def test_get_informationmodels_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_informationmodels())


@pytest.mark.unit
def test_get_organization_from_organization_catalogue_should_throw_bad_uri_exception(event_loop, mocker):
    pass


@pytest.mark.unit
def test_get_organization_from_organization_catalogue_should_return_json_organization(event_loop, mocker):
    pass


@pytest.mark.unit
def test_get_organization_from_alternative_registry_should_return_parsed_organization(event_loop, mocker):
    pass


@pytest.mark.unit
def test_get_organization_from_alternative_registry_should_throw_bad_uri_exception(event_loop, mocker):
    pass


class HttpResponseMock:
    def __init__(self, status):
        self.status_code = status
        self.request = {}


def get_orgpath_mock(name):
    return f"/ANNET/{name}"


@pytest.mark.unit
def test_get_organization_should_return_default_organization(event_loop, mocker):
    pass
