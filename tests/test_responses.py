import pytest

from src.responses import OrganizationCatalogResponse, OrganizationCatalogListResponse
from src.result_readers import ParsedContent
from tests.test_data import org_5, org4, org_1, org_3, default_org


@pytest.mark.unit
def test_organization_catalog_response():
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

    result = OrganizationCatalogResponse(organization=org_5,
                                         datasets=ParsedContent(count=3, name=org_5["name"],
                                                                org_id=org_5["norwegianRegistry"]),
                                         dataservices=ParsedContent(count=100, name=org_5["name"],
                                                                    org_id=org_5["organizationId"]),
                                         concepts=None,
                                         informationmodels=ParsedContent(count=200, name=org_5["name"],
                                                                         org_id=org_5["norwegianRegistry"])
                                         ).__dict__
    assert result == expected


@pytest.mark.unit
def test_organization_without_prefLabel_catalog_response():
    expected = {
        "id": "961181399",
        "organization": {
            "name": {
                "no": "ARKIVVERKET"
            },
            "orgPath": "/STAT/972417866/961181399"
        },
        "dataset_count": 3,
        "concept_count": 0,
        "dataservice_count": 100,
        "informationmodel_count": 200
    }

    result = OrganizationCatalogResponse(organization=org4,
                                         datasets=ParsedContent(count=3, name=org4["name"],
                                                                org_id=org4["norwegianRegistry"]),
                                         dataservices=ParsedContent(count=100, name=org4["name"],
                                                                    org_id=org4["organizationId"]),
                                         concepts=None,
                                         informationmodels=ParsedContent(count=200, name=org4["name"],
                                                                         org_id=org4["norwegianRegistry"])
                                         ).__dict__
    assert result == expected


@pytest.mark.unit
def test_organization_catalog_list_response():
    org_catalog_1 = OrganizationCatalogResponse(organization=org_1,
                                                datasets=ParsedContent(count=3, name=org_1["name"],
                                                                       org_id=org_1["norwegianRegistry"]),
                                                dataservices=ParsedContent(count=100, name=org_1["name"],
                                                                           org_id=org_1["organizationId"]),
                                                concepts=ParsedContent(count=200, name=org_1["name"],
                                                                       org_id=org_1[
                                                                           "norwegianRegistry"]),
                                                informationmodels=ParsedContent(count=200, name=org_1["name"],
                                                                                org_id=org_1[
                                                                                    "norwegianRegistry"])
                                                )
    org_catalog_2 = OrganizationCatalogResponse(organization=org4,
                                                datasets=ParsedContent(count=3, name=org4["name"],
                                                                       org_id=org4["norwegianRegistry"]),
                                                dataservices=ParsedContent(count=100, name=org4["name"],
                                                                           org_id=org4["organizationId"]),
                                                concepts=ParsedContent(count=200, name=org4["name"],
                                                                       org_id=org4[
                                                                           "norwegianRegistry"]),
                                                informationmodels=ParsedContent(count=200, name=org4["name"],
                                                                                org_id=org_1[
                                                                                    "norwegianRegistry"])
                                                )
    org_catalog_3 = OrganizationCatalogResponse(organization=org_3,
                                                datasets=ParsedContent(count=3, name=org_3["name"],
                                                                       org_id=org_3["norwegianRegistry"]),
                                                dataservices=ParsedContent(count=100, name=org_3["name"],
                                                                           org_id=org_3["organizationId"]),
                                                concepts=ParsedContent(count=200, name=org_3["name"],
                                                                       org_id=org_3[
                                                                           "norwegianRegistry"]),
                                                informationmodels=ParsedContent(count=200, name=org_3["name"],
                                                                                org_id=org_3[
                                                                                    "norwegianRegistry"])
                                                )

    list_response = OrganizationCatalogListResponse()
    list_response.add_organization_catalog(org_catalog_1)
    list_response.add_organization_catalog(org_catalog_2)
    list_response.add_organization_catalog(org_catalog_3)

    result = list_response.map_response()

    assert result.keys().__len__() == 1 and "organizations" in result.keys()
    assert result["organizations"].__len__() == 3


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
    result = OrganizationCatalogResponse(organization=default_org,
                                         datasets=ParsedContent(count=3, name=org4["name"],
                                                                org_id=org4["norwegianRegistry"]),
                                         dataservices=ParsedContent(count=100, name=org4["name"],
                                                                    org_id=org4["organizationId"]),
                                         concepts=None,
                                         informationmodels=ParsedContent(count=29, name=org4["name"],
                                                                         org_id=org4["norwegianRegistry"])
                                         ).__dict__
    assert result == expected
