import pytest
import requests

from src.service_requests import get_organizations, ServiceKey, get_concepts_for_organization, \
    get_datasets_for_organization, get_informationmodels_for_organization
from src.utils import FetchFromServiceException

get_request = "src.service_requests.requests.get"

service_urls = {
    ServiceKey.ORGANIZATIONS: "http://localhost:8080/organizations",
    ServiceKey.INFO_MODELS: "http://localhost:8080/informationmodels",
    ServiceKey.DATA_SERVICES: "http://localhost:8080/apis",
    ServiceKey.DATA_SETS: "http://localhost:8080/datasets",
    ServiceKey.CONCEPTS: "http://localhost:8080/concepts"

}


@pytest.mark.unit
def test_get_organizations(mock_get_services_request):
    get_organizations()
    mock_get_services_request.assert_called_once_with(url="http://localhost:8080/organizations", timeout=10)


@pytest.mark.unit
def test_get_organizations_should_throw_error(mocker):
    mocker.patch(get_request, side_effect=requests.ConnectionError())
    with pytest.raises(FetchFromServiceException) as err:
        get_organizations()


@pytest.mark.unit
def test_get_concepts_for_organization(mock_get_services_request):
    get_concepts_for_organization(orgPath="12345")
    mock_get_services_request.assert_called_once_with(url=service_urls[ServiceKey.CONCEPTS] + "?orgPath=12345",
                                                      timeout=10)


@pytest.mark.unit
def test_get_concepts_for_organization_should_throw_error(mocker):
    mocker.patch(get_request, side_effect=requests.ConnectionError())
    with pytest.raises(FetchFromServiceException) as err:
        get_concepts_for_organization(orgPath="12345")


@pytest.mark.unit
def test_get_datasets_for_organization(mock_get_services_request):
    get_datasets_for_organization(orgPath="12345")
    assert mock_get_services_request.called_once_with(url=service_urls[ServiceKey.DATA_SETS] + "?orgPath=12345",
                                                      tiemout=10)


@pytest.mark.unit
def test_get_datasets_for_organization_should_throw_error(mocker):
    mocker.patch(get_request, side_effect=requests.ConnectionError)
    with pytest.raises(FetchFromServiceException) as err:
        get_datasets_for_organization(orgPath="12345")


@pytest.mark.unit
def test_get_dataservices_for_organization(mock_get_services_request):
    get_concepts_for_organization(orgPath="12345")
    assert mock_get_services_request.called_once_with(url=service_urls[ServiceKey.DATA_SERVICES] + "?orgPath=12345",
                                                      timeout=10)


@pytest.mark.unit
def test_get_dataservices_for_organization_should_throw_error(mocker):
    mocker.patch(get_request, side_effect=requests.ConnectionError())
    with pytest.raises(FetchFromServiceException) as err:
        get_datasets_for_organization(orgPath="12345")


@pytest.mark.unit
def test_get_informationmodels_for_organization(mock_get_services_request):
    get_concepts_for_organization(orgPath="12345")
    assert mock_get_services_request.called_once_with(url=service_urls[ServiceKey.INFO_MODELS] + "?orgPath=12345",
                                                      timeout=10)


@pytest.mark.unit
def test_get_informationmodels_for_organization_should_throw_error(mocker):
    mocker.patch(get_request, side_effect=requests.ConnectionError())
    with pytest.raises(FetchFromServiceException) as err:
        get_informationmodels_for_organization(orgPath="12345")
