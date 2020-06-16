import pytest

from src.aggregation import aggregate_results
from src.responses import OrganizationCatalogListResponse
from src.result_readers import ParsedContent
from tests.test_data import org_1, org_2, parsed_org_from_geonorge


def parsed_response_with_uri(count, organization):
    return ParsedContent(count=count, name=organization["name"], org_id=organization["norwegianRegistry"])


def parsed_response_with_id(count, organization):
    return ParsedContent(count=count, name=organization["name"], org_id=organization["organizationId"])


def default_org(name):
    return {
        "prefLabel": {
            "no": name
        },
        "orgPath": f"ANNET/{name}",
        "name": name
    }


@pytest.mark.unit
def test_aggregate_result_should_return_catalog_list_response(mocker):
    get_org_mock = mocker.patch('src.aggregation.get_organization', return_value={})
    result: OrganizationCatalogListResponse = \
        aggregate_results(organizations_from_service=[org_1, org_2],
                          concepts=[parsed_response_with_uri(count=3,
                                                             organization=org_1)],
                          dataservices=[parsed_response_with_id(count=5,
                                                                organization=org_1),
                                        parsed_response_with_id(count=1115,
                                                                organization=org_2)],
                          datasets=[parsed_response_with_uri(count=76,
                                                             organization=org_2)],
                          informationmodels=[parsed_response_with_uri(count=22,
                                                                      organization=org_1),
                                             parsed_response_with_uri(count=58,
                                                                      organization=org_2)]
                          )
    assert result.count() == 2
    org_1_result: dict = result.org_list[0]
    org_2_result: dict = result.org_list[1]
    assert get_org_mock.await_count == 0
    assert org_1_result["id"] == org_1["organizationId"]
    assert org_1_result["organization"]["orgPath"] == org_1["orgPath"]
    assert org_1_result["dataset_count"] == 0
    assert org_1_result["concept_count"] == 3
    assert org_1_result["informationmodel_count"] == 22
    assert org_1_result["dataservice_count"] == 5
    assert org_2_result["id"] == org_2["organizationId"]
    assert org_2_result["organization"]["orgPath"] == org_2["orgPath"]
    assert org_2_result["dataset_count"] == 76
    assert org_2_result["concept_count"] == 0
    assert org_2_result["informationmodel_count"] == 58
    assert org_2_result["dataservice_count"] == 1115


@pytest.mark.unit
def test_aggregate_result_should_return_catalog_list_response_with_new_organization_by_uri(mocker):
    get_org_count = mocker.patch('src.aggregation.get_organization', return_value=org_1)
    result: OrganizationCatalogListResponse = \
        aggregate_results(organizations_from_service=[org_2],
                          concepts=[parsed_response_with_uri(count=3,
                                                             organization=org_1)],
                          dataservices=[parsed_response_with_id(count=1115,
                                                                organization=org_2)],
                          datasets=[parsed_response_with_uri(count=76,
                                                             organization=org_2)],
                          informationmodels=[parsed_response_with_uri(count=22,
                                                                      organization=org_1),
                                             parsed_response_with_uri(count=58,
                                                                      organization=org_2)]
                          )
    assert result.count() == 2
    assert get_org_count.await_count == 1
    org_1_result: dict = result.org_list[1]
    org_2_result: dict = result.org_list[0]
    assert org_1_result["organization"]["orgPath"] == org_1["orgPath"]
    assert org_1_result["dataset_count"] == 0
    assert org_1_result["concept_count"] == 3
    assert org_1_result["informationmodel_count"] == 22
    assert org_1_result["dataservice_count"] == 0
    assert org_2_result["organization"]["orgPath"] == org_2["orgPath"]
    assert org_2_result["dataset_count"] == 76
    assert org_2_result["concept_count"] == 0
    assert org_2_result["informationmodel_count"] == 58
    assert org_2_result["dataservice_count"] == 1115


@pytest.mark.unit
def test_aggregate_result_should_return_catalog_list_response_with_mixed_alt_and_norwegian_ir(mocker):
    get_org_mock = mocker.patch('src.aggregation.get_organization', return_value=parsed_org_from_geonorge)
    result: OrganizationCatalogListResponse = \
        aggregate_results(organizations_from_service=[org_2],
                          concepts=[parsed_response_with_id(count=3,
                                                            organization=parsed_org_from_geonorge)],
                          dataservices=[parsed_response_with_id(count=1115,
                                                                organization=parsed_org_from_geonorge)],
                          datasets=[parsed_response_with_id(count=76,
                                                            organization=org_2)],
                          informationmodels=[parsed_response_with_id(count=22,
                                                                     organization=parsed_org_from_geonorge),
                                             parsed_response_with_id(count=58,
                                                                     organization=org_2)]
                          )
    assert result.count() == 2
    assert get_org_mock.await_count == 1
    geo_norge_result: dict = result.org_list[1]
    org_2_result: dict = result.org_list[0]
    assert geo_norge_result["organization"]["orgPath"] == parsed_org_from_geonorge["orgPath"]
    assert geo_norge_result["concept_count"] == 3
    assert geo_norge_result["dataservice_count"] == 1115
    assert geo_norge_result["dataset_count"] == 0
    assert geo_norge_result["informationmodel_count"] == 22
    assert org_2_result["organization"]["orgPath"] == org_2["orgPath"]
    assert org_2_result["concept_count"] == 0
    assert org_2_result["dataservice_count"] == 0
    assert org_2_result["dataset_count"] == 76
    assert org_2_result["informationmodel_count"] == 58


def test_aggregate_result_should_return_catalog_list_response_with_mixed_alt_norwegian_and_default_id(mocker):
    get_org_mock = mocker.patch('src.aggregation.get_organization', return_value=parsed_org_from_geonorge)
    result: OrganizationCatalogListResponse = \
        aggregate_results(organizations_from_service=[org_2],
                          concepts=[parsed_response_with_id(count=3,
                                                            organization=parsed_org_from_geonorge)],
                          dataservices=[parsed_response_with_id(count=1115,
                                                                organization=parsed_org_from_geonorge)],
                          datasets=[parsed_response_with_id(count=76,
                                                            organization=org_2)],
                          informationmodels=[parsed_response_with_id(count=22,
                                                                     organization=parsed_org_from_geonorge),
                                             parsed_response_with_id(count=58,
                                                                     organization=org_2)]
                          )
    assert result.count() == 2
    assert get_org_mock.await_count == 1
    geo_norge_result: dict = result.org_list[1]
    org_2_result: dict = result.org_list[0]
    assert geo_norge_result["organization"]["orgPath"] == parsed_org_from_geonorge["orgPath"]
    assert geo_norge_result["concept_count"] == 3
    assert geo_norge_result["dataservice_count"] == 1115
    assert geo_norge_result["dataset_count"] == 0
    assert geo_norge_result["informationmodel_count"] == 22
    assert org_2_result["organization"]["orgPath"] == org_2["orgPath"]
    assert org_2_result["concept_count"] == 0
    assert org_2_result["dataservice_count"] == 0
    assert org_2_result["dataset_count"] == 76
    assert org_2_result["informationmodel_count"] == 58
