import asyncio

import pytest

from src.organization_utils import get_organization, get_generated_org_path
from src.result_readers import OrganizationReferencesObject
from src.utils import NotInNationalRegistryException, ServiceKey, OrganizationCatalogResult


@pytest.mark.unit
def test_get_organization_should_return_none(event_loop):
    test_org = OrganizationReferencesObject(
        for_service=ServiceKey.INFO_MODELS,
        org_uri="http_no_plz"
    )
    assert event_loop.run_until_complete(get_organization(test_org.id, test_org.name)) is None


@pytest.mark.unit
def test_get_organization_should_return_catalog_response_by_id(event_loop, mock_fetch_organization_with_id):
    test_org = OrganizationReferencesObject(
        for_service=ServiceKey.INFO_MODELS,
        org_uri="https://data.brreg.no/123",
        name="Some name"
    )
    test_org_id_only = OrganizationReferencesObject(
        for_service=ServiceKey.INFO_MODELS,
        org_uri="https://data.brreg.no/123",
        name="Some name"
    )
    test_org_name_only = OrganizationReferencesObject(
        for_service=ServiceKey.INFO_MODELS,
        org_uri="https://data.brreg.no/123",
        name="Some name"
    )
    result, result_id, result_name = event_loop.run_until_complete(
        asyncio.gather(
            get_organization(test_org.id, test_org.name),
            get_organization(test_org_id_only.id, test_org_id_only.name),
            get_organization(test_org_name_only.id, test_org_name_only.name)
        )
    )
    expected_values = fetch_org_mock_id()
    assert result is not None
    assert result.org_id == expected_values.org_id
    assert result.name == expected_values.name
    assert result.org_path == expected_values.org_path
    assert result_id is not None
    assert result_id.org_id == expected_values.org_id
    assert result_id.name == expected_values.name
    assert result_id.org_path == expected_values.org_path
    assert result_name is not None
    assert result_name.org_id == expected_values.org_id
    assert result_name.name == expected_values.name
    assert result_name.org_path == expected_values.org_path


@pytest.mark.unit
def test_get_organization_should_return_generated_org_path(event_loop,
                                                           mock_fetch_organization_not_in_national_registry,
                                                           mock_get_generated_org_path):
    test_org_name_only = OrganizationReferencesObject(
        for_service=ServiceKey.INFO_MODELS,
        org_uri="https://data.brreg.no/123",
        name="Some Name"
    )
    result = event_loop.run_until_complete(get_organization(test_org_name_only.id, test_org_name_only.name))
    assert result.org_path == "/ANNET/Some Name"


@pytest.mark.unit
def test_get_generated_org_path_should_return_none(event_loop):
    test_org = OrganizationReferencesObject(
        for_service=ServiceKey.INFO_MODELS
    )
    result = event_loop.run_until_complete(get_generated_org_path(name=test_org.name))
    assert result is None


@pytest.mark.unit
def test_get_generated_org_path_should_return_orgpath(event_loop,mock_get_generated_org_path):
    test_on_name = OrganizationReferencesObject(
        for_service=ServiceKey.INFO_MODELS,
        name="Some Name"
    )
    result = event_loop.run_until_complete(get_generated_org_path(name=test_on_name.name))
    assert result == "/ANNET/Some Name"


def fetch_org_mock_id() -> OrganizationCatalogResult:
    return OrganizationCatalogResult(
        org_id=123,
        name="Some name",
        org_path="/PRIVAT/123"
    )


def not_in_national():
    raise NotInNationalRegistryException("Not found")


@pytest.fixture
def mock_fetch_organization_with_id(mocker):
    return mocker.patch('src.organization_utils.fetch_organization_by_id', return_value=fetch_org_mock_id())


@pytest.fixture
def mock_fetch_organization_not_in_national_registry(mocker):
    return mocker.patch('src.organization_utils.fetch_organization_by_id',
                        side_effect=NotInNationalRegistryException("tadda"))


@pytest.fixture
def mock_get_generated_org_path(mocker):
    return mocker.patch('src.organization_utils.fetch_generated_org_path_from_organization_catalog',
                        return_value="/ANNET/Some Name")
