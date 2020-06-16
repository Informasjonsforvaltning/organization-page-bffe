import pytest
from httpcore import ConnectError
from httpx import HTTPError
from src.service_requests import ServiceKey, get_organizations, get_concepts, get_datasets, get_dataservices, \
    get_informationmodels, get_organization_from_organization_catalogue, get_organization_from_alternative_registry, \
    get_organization
from src.result_readers import ParsedContent
from src.utils import FetchFromServiceException, BadUriException
from tests.conftest import get_xhttp_mock
from tests.test_data import org_1, geonorge_rdf_organization, parsed_org_from_geonorge

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
    event_loop.run_until_complete(get_organizations())
    mock_get_xhttp_organizations.assert_called_once_with(url="http://localhost:8080/organizations",
                                                         headers={"Accept": "application/json"},
                                                         timeout=5)


@pytest.mark.unit
def test_get_organizations_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_organizations())


@pytest.mark.unit
def test_get_concepts_should_get_all_concepts(event_loop, mocker):
    mocker.patch(get_request,
                 return_value=get_xhttp_mock(status_code=200, service_key=ServiceKey.CONCEPTS))
    result = event_loop.run_until_complete(get_concepts())
    assert result.__len__() == 2
    assert result[0].count == 5
    assert result[1].count == 5


@pytest.mark.unit
def test_get_concepts_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_concepts())


@pytest.mark.unit
def test_get_datasets_should_return_parsed_table(event_loop, mocker):
    mock_values = get_xhttp_mock(status_code=200, service_key=ServiceKey.DATA_SETS, organizations=[org_1])
    mocker.patch('httpx.AsyncClient.get', return_value=mock_values)
    result = event_loop.run_until_complete(get_datasets())
    first_result = result[0]
    assert isinstance(first_result, ParsedContent)


@pytest.mark.unit
def test_get_datasets_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_datasets())


@pytest.mark.unit
def test_get_dataservices_should_get_all_dataservices(event_loop, mocker):
    mocker.patch(get_request,
                 return_value=get_xhttp_mock(status_code=200, service_key=ServiceKey.DATA_SERVICES))
    result = event_loop.run_until_complete(get_dataservices())
    assert result.__len__() == 1
    assert result[0].count == 21


@pytest.mark.unit
def test_get_dataservices_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_dataservices())


@pytest.mark.unit
def test_get_informationmodels_should_get_all_models(event_loop, mocker):
    mocker.patch(get_request,
                 return_value=get_xhttp_mock(status_code=200, service_key=ServiceKey.INFO_MODELS))
    result = event_loop.run_until_complete(get_informationmodels())
    assert result.__len__() == 1
    assert result[0].count == 7


@pytest.mark.unit
def test_get_informationmodels_should_throw_error(event_loop, mocker):
    mocker.patch(get_request, side_effect=ConnectError())
    with pytest.raises(FetchFromServiceException):
        event_loop.run_until_complete(get_informationmodels())


@pytest.mark.unit
def test_get_organization_from_organization_catalogue_should_throw_bad_uri_exception(event_loop, mocker):
    mocker.patch(get_request, side_effect=HTTPError(response=HttpResponseMock(404)))
    with pytest.raises(BadUriException):
        event_loop.run_until_complete(get_organization_from_organization_catalogue(organization_id="567724"))


@pytest.mark.unit
def test_get_organization_from_organization_catalogue_should_return_json_organization(event_loop, mocker):
    get_mock = mocker.patch(get_request,
                            return_value=get_xhttp_mock(status_code=200, json={
                                "organizationId": "974760673",
                                "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
                                "name": "REGISTERENHETEN I BRØNNØYSUND",
                                "orgType": "ORGL",
                                "orgPath": "STAT/912660680/974760673",
                                "subOrganizationOf": "912660680",
                                "issued": "1995-08-09",
                                "municipalityNumber": "1813",
                                "industryCode": "84.110",
                                "sectorCode": "6100",
                            }))
    result = event_loop.run_until_complete(get_organization_from_organization_catalogue(974760673))
    assert get_mock.called_once_with(url=f"{service_urls[ServiceKey.ORGANIZATIONS]}/974760673",
                                     headers={"Accept": "application/json"},
                                     timeout=1)
    assert isinstance(result, dict)


@pytest.mark.unit
def test_get_organization_from_alternative_registry_should_return_parsed_organization(event_loop, mocker):
    mocker.patch(get_request, return_value=get_xhttp_mock(status_code=200, text=geonorge_rdf_organization))
    result = event_loop.run_until_complete(
        get_organization_from_alternative_registry(organization_iri="http://oneofthegoodones/56725740")
    )
    assert result == parsed_org_from_geonorge


@pytest.mark.unit
def test_get_organization_from_alternative_registry_should_throw_bad_uri_exception(event_loop, mocker):
    mocker.patch(get_request, side_effect=HTTPError(response=HttpResponseMock(404)))
    with pytest.raises(BadUriException):
        event_loop.run_until_complete(
            get_organization_from_alternative_registry(organization_iri="http://oneofthebadones/56725740"))


@pytest.mark.unit
def test_get_organization_from_alternative_registry_should_throw_bad_uri_exception_for_html(event_loop, mocker):
    mocker.patch(get_request, return_value=get_xhttp_mock(status_code=200, text="""<!DOCTYPE html>"""))
    with pytest.raises(BadUriException):
        event_loop.run_until_complete(
            get_organization_from_alternative_registry(organization_iri="http://oneofthebadones/56725740"))


class HttpResponseMock:
    def __init__(self, status):
        self.status_code = status
        self.request = {}


@pytest.mark.unit
def test_get_organization_should_return_default_organization(event_loop, mocker):
    mocker.patch('src.service_requests.get_organization_from_alternative_registry',
                 side_effect=BadUriException(execution_point="lkaslfa"))
    result = event_loop.run_until_complete(get_organization(
        missing_organization=ParsedContent(
            name="sjfdlk",
            org_id="https://hjafdkahsfk.hasfjk",
            count=789)))
    assert result == {
        "prefLabel": {
            "no": "sjfdlk"
        },
        "orgPath": "ANNET/sjfdlk"
    }
