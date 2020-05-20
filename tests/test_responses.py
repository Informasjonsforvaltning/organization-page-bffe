import json

import pytest

from src.responses import OrganizationCatalogResponse, OrganizationCatalogListResponse
from tests.test_data import org_5, concept_response, dataset_response, \
    dataservice_response, info_model_response, org4, org_1, org_5_without_prefLabel_object


@pytest.mark.unit
def test_organization_catalog_response():
    expected = {
        "id": "915429785",
        "organization": {
            "name": {
                "no": "POLITI- OG LENSMANNSETATEN"
            },
            "orgPath": "STAT/972417831/915429785"
        },
        "dataset_count": 3,
        "concept_count": 0,
        "dataservice_count": 100,
        "informationmodel_count": 200
    }

    result = OrganizationCatalogResponse(organization=org_5,
                                         datasets=dataset_response(3),
                                         dataservices=dataservice_response(100),
                                         concepts=concept_response(0),
                                         informationmodels=info_model_response(200)
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
            "orgPath": "STAT/972417866/961181399"
        },
        "dataset_count": 3,
        "concept_count": 0,
        "dataservice_count": 100,
        "informationmodel_count": 200
    }

    result = OrganizationCatalogResponse(organization=org4,
                                         datasets=dataset_response(3),
                                         dataservices=dataservice_response(100),
                                         concepts=concept_response(0),
                                         informationmodels=info_model_response(200)
                                         ).__dict__
    assert result == expected


@pytest.mark.unit
def test_organization_catalog_list_response():
    org_catalog_1 = OrganizationCatalogResponse(organization=org_5,
                                                datasets=dataset_response(3),
                                                dataservices=dataservice_response(100),
                                                concepts=concept_response(0),
                                                informationmodels=info_model_response(200)
                                                )
    org_catalog_2 = OrganizationCatalogResponse(organization=org4,
                                                datasets=dataset_response(3),
                                                dataservices=dataservice_response(100),
                                                concepts=concept_response(0),
                                                informationmodels=info_model_response(200)
                                                )
    org_catalog_3 = OrganizationCatalogResponse(organization=org_1,
                                                datasets=dataset_response(3),
                                                dataservices=dataservice_response(100),
                                                concepts=concept_response(0),
                                                informationmodels=info_model_response(200)
                                                )


    list_response = OrganizationCatalogListResponse()
    list_response.add_organization_catalog(org_catalog_1)
    list_response.add_organization_catalog(org_catalog_2)
    list_response.add_organization_catalog(org_catalog_3)

    result = list_response.map_response()

    assert result.keys().__len__() == 1 and "organizations" in result.keys()
    assert result["organizations"].__len__() == 3