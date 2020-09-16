import pytest

from src.responses import OrganizationCatalogResponse, OrganizationCatalogListResponse
from src.result_readers import OrganizationReferencesObject, OrganizationStore
from src.utils import ServiceKey


@pytest.mark.unit
def test_organization_to_response_dict():
    expected = {
        "id": "915429785",
        "organization": {
            "name": {
                "no": "POLITI- OG LENSMANNSETATEN"
            },
            "orgPath": "/STAT/972417831/915429785"
        },
        "dataset_count": 3,
        "concept_count": 0,
        "dataservice_count": 100,
        "informationmodel_count": 200
    }

    org_ref = OrganizationReferencesObject(
        name="POLITI- OG LENSMANNSETATEN",
        org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/915429785",
        org_path="/STAT/972417831/915429785",
        for_service=ServiceKey.ORGANIZATIONS
    )
    org_ref.set_count_value(for_service=ServiceKey.DATASETS, count=3)
    org_ref.set_count_value(for_service=ServiceKey.CONCEPTS, count=0)
    org_ref.set_count_value(for_service=ServiceKey.DATA_SERVICES, count=100)
    org_ref.set_count_value(for_service=ServiceKey.INFO_MODELS, count=200)
    assert OrganizationCatalogResponse(organization=org_ref).__dict__ == expected


@pytest.mark.unit
def test_organization_catalog_without_id():
    expected = {
        "organization": {
            "name": {
                "no": "BurdeSkjerpeSeg"
            },
            "orgPath": f"/ANNET/BurdeSkjerpeSeg"
        },
        "dataset_count": 3,
        "concept_count": 0,
        "dataservice_count": 100,
        "informationmodel_count": 29
    }
    org_ref = OrganizationReferencesObject(
        name="BurdeSkjerpeSeg",
        org_path="/ANNET/BurdeSkjerpeSeg",
        for_service=ServiceKey.ORGANIZATIONS
    )
    org_ref.dataset_count = 3
    org_ref.dataservice_count = 100
    org_ref.informationmodel_count = 29
    assert OrganizationCatalogResponse(organization=org_ref).__dict__ == expected


@pytest.mark.unit
def test_organization_catalog_without_id():
    expected = {
        "organization": {
            "name": {
                "no": "BurdeSkjerpeSeg"
            },
            "orgPath": f"/ANNET/BurdeSkjerpeSeg"
        },
        "dataset_count": 3,
        "concept_count": 0,
        "dataservice_count": 100,
        "informationmodel_count": 29
    }
    org_ref = OrganizationReferencesObject(
        name="BurdeSkjerpeSeg",
        org_path="/ANNET/BurdeSkjerpeSeg",
        for_service=ServiceKey.ORGANIZATIONS
    )
    org_ref.dataset_count = 3
    org_ref.dataservice_count = 100
    org_ref.informationmodel_count = 29
    assert OrganizationCatalogResponse(organization=org_ref).__dict__ == expected


@pytest.mark.unit
def test_organization_catalog_list_response():
    politi_ref = OrganizationReferencesObject(
        name="POLITI- OG LENSMANNSETATEN",
        org_path="/STAT/972417831/915429785",
        org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/915429785",
        count=3,
        for_service=ServiceKey.DATASETS)
    some_other_ref = OrganizationReferencesObject(
        name="STRANDA SAG- OG HØVLERI",
        org_path="/PRIVAT/1256847",
        org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/1256847",
        count=88,
        for_service=ServiceKey.CONCEPTS)
    one_empty_ref = OrganizationReferencesObject(
        name="EMPTY NONSENSE",
        org_path="/ANNET/1256847",
        for_service=ServiceKey.ORGANIZATIONS)
    politi_parent_ref = OrganizationReferencesObject(
        name="LOVER OG SÅNNE TING",
        org_path="/STAT/972417831",
        org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/972417831",
        count=99,
        for_service=ServiceKey.DATASETS)
    politi_root_orgpath_ref = OrganizationReferencesObject(
        name="Stat",
        org_path="/STAT",
        count=99,
        for_service=ServiceKey.DATASETS)

    store = OrganizationStore.get_instance()
    store.organizations = []
    store.add_organization(organization=politi_parent_ref, for_service=ServiceKey.DATASETS)
    store.add_organization(organization=politi_ref, for_service=ServiceKey.DATASETS)
    store.add_organization(organization=politi_root_orgpath_ref, for_service=ServiceKey.DATASETS)
    store.add_organization(organization=one_empty_ref)
    store.add_organization(some_other_ref)

    result = OrganizationCatalogListResponse.from_organization_store(organization_store=store)
    assert result.count() == 2
    assert result.org_list[0]["organization"]["name"]["no"] == "POLITI- OG LENSMANNSETATEN"
    assert result.org_list[1]["organization"]["name"]["no"] == "STRANDA SAG- OG HØVLERI"
