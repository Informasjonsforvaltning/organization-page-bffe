import pytest

from src.responses import OrganizationCatalogResponse, OrganizationCatalogListResponse
from tests.test_data import org_politi, org4, org_brreg, org_3, default_org


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
    pytest.xfail()


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

    pytest.xfail()


@pytest.mark.unit
def test_organization_catalog_list_response():
    pytest.xfail()


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
    pytest.xfail()
