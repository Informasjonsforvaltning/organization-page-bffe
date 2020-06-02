import pytest
from httpcore import ConnectError

from src.service_requests import ServiceKey, get_concepts_for_organization, \
    get_datasets_for_organization, get_informationmodels_for_organization, get_organizations_async
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
def test_get_organizations_async(event_loop, mock_get_xhttp_organizations):
    event_loop.run_until_complete(get_organizations_async())
    mock_get_xhttp_organizations.assert_called_once_with(url="http://localhost:8080/organizations",
                                                         headers={"Accept": "application/json"},
                                                         timeout=10)


@pytest.mark.unit
def test_get_organizations_async_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_organizations_async())


@pytest.mark.unit
def test_get_concepts_for_organization(event_loop, mock_get_xhttp_concepts):
    event_loop.run_until_complete(get_concepts_for_organization(orgPath="12345"))
    mock_get_xhttp_concepts.assert_awaited_once_with(url=service_urls[ServiceKey.CONCEPTS] + "?orgPath=12345",
                                                     timeout=10)


@pytest.mark.unit
def test_get_concepts_for_organization_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_concepts_for_organization(orgPath="12345"))


@pytest.mark.unit
def test_get_datasets_for_organization(event_loop, mock_get_xhttp_datasets):
    event_loop.run_until_complete(get_datasets_for_organization(orgPath="12345"))
    assert mock_get_xhttp_datasets.awaited_once_with(url=service_urls[ServiceKey.DATA_SETS] + "?orgPath=12345",
                                                     tiemout=10)


@pytest.mark.unit
def test_get_datasets_for_organization_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_datasets_for_organization(orgPath="12345"))


@pytest.mark.unit
def test_get_dataservices_for_organization(event_loop, mock_get_xhttp_dataservices):
    event_loop.run_until_complete(get_concepts_for_organization(orgPath="12345"))
    assert mock_get_xhttp_dataservices.awaited_once_with(
        url=service_urls[ServiceKey.DATA_SERVICES] + "?orgPath=12345",
        timeout=10)


@pytest.mark.unit
def test_get_dataservices_for_organization_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_datasets_for_organization(orgPath="12345"))


@pytest.mark.unit
def test_get_informationmodels_for_organization(event_loop, mock_get_xhttp_informationmodels):
    event_loop.run_until_complete(get_informationmodels_for_organization("12345"))
    assert mock_get_xhttp_informationmodels.awaited_once_with(
        url=service_urls[ServiceKey.INFO_MODELS] + "?orgPath=12345",
        timeout=10)


@pytest.mark.unit
def test_get_informationmodels_for_organization_should_send_second_request(event_loop,
                                                                           mock_get_xhttp_informationmodels_empty):
    event_loop.run_until_complete(get_informationmodels_for_organization(orgPath="12345"))
    assert mock_get_xhttp_informationmodels_empty.call_count == 2
    assert mock_get_xhttp_informationmodels_empty.called_with(
        url=service_urls[ServiceKey.INFO_MODELS] + "?orgPath=/12345",
        timeout=10)
    assert mock_get_xhttp_informationmodels_empty.called_with(
        url=service_urls[ServiceKey.INFO_MODELS] + "?orgPath=12345",
        timeout=10)


@pytest.mark.unit
def test_get_informationmodels_for_organization_should_throw_error(event_loop,mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_informationmodels_for_organization(orgPath="12345"))
