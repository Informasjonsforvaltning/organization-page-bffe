import pytest

from src.aggregation import combine_results
from src.result_readers import OrganizationStore, OrganizationReferencesObject
from src.utils import ServiceKey


@pytest.mark.unit
def test_combine_results_should_update_organization_store_with_one_organization():
    catalog_org = [
        OrganizationReferencesObject.from_organization_catalog_single_response(
            {
                "organizationId": "974760673",
                "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
                "internationalRegistry": None,
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgType": "ORGL",
                "orgPath": "/STAT/912660680/974760673",
                "subOrganizationOf": "912660680",
                "issued": "1995-08-09",
                "municipalityNumber": "1813",
                "industryCode": "84.110",
                "sectorCode": "6100",
                "prefLabel": None,
                "allowDelegatedRegistration": None
            })
    ]
    info_model_aggregations = [
        OrganizationReferencesObject.from_es_response(
            es_response={
                "key": "/STAT",
                "count": 33
            },
            for_service=ServiceKey.INFO_MODELS
        ),
        OrganizationReferencesObject.from_es_response(
            es_response={
                "key": "/STAT/912660680",
                "count": 33
            },
            for_service=ServiceKey.INFO_MODELS
        ),
        OrganizationReferencesObject.from_es_response(
            es_response={
                "key": "/STAT/912660680/974760673",
                "count": 33
            },
            for_service=ServiceKey.INFO_MODELS
        )
    ]
    concept_aggregations = [
        OrganizationReferencesObject.from_es_response(
            es_response={
                "key": "/STAT",
                "count": 23
            },
            for_service=ServiceKey.CONCEPTS
        ),
        OrganizationReferencesObject.from_es_response(
            es_response={
                "key": "/STAT/912660680",
                "count": 23
            },
            for_service=ServiceKey.CONCEPTS
        ),
        OrganizationReferencesObject.from_es_response(
            es_response={
                "key": "/STAT/912660680/974760673",
                "count": 23
            },
            for_service=ServiceKey.CONCEPTS
        )

    ]

    dataset_result = [
        OrganizationReferencesObject.from_sparql_query_result(
            for_service=ServiceKey.DATASETS,
            organization={
                "sameAs": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673"
                },
                "name": {
                    "type": "literal",
                    "value": "REGISTERENHETEN I BRØNNØYSUND"
                },
                "count": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                    "value": "2"
                }
            }
        ),
        OrganizationReferencesObject.from_sparql_query_result(
            for_service=ServiceKey.DATASETS,
            organization={
                "publisher": {
                    "type": "uri",
                    "value": "https://natonational.no/api/enheter/987498as24sfw"
                },
                "name": {
                    "type": "literal",
                    "value": "REGISTERENHETEN I BRØNNØYSUND"
                },
                "count": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                    "value": "2"
                }
            }
        )

    ]
    data_services_result = [
        OrganizationReferencesObject.from_sparql_query_result(
            for_service=ServiceKey.DATA_SERVICES,
            organization={
                "publisher": {
                    "type": "uri",
                    "value": "https://organization-catalogue.staging.fellesdatakatalog.digdir.no/organizations"
                             "/974760673 "
                },
                "count": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                    "value": "18"
                }
            }
        )
    ]

    combine_results(
        organizations_from_service=catalog_org,
        concepts=concept_aggregations,
        informationmodels=info_model_aggregations,
        datasets=dataset_result,
        dataservices=data_services_result
    )

    store = OrganizationStore.get_instance()
    org_list = store.get_organization_list()
    assert len(org_list) == 1
    test_org = org_list[0]
    assert test_org.name == "REGISTERENHETEN I BRØNNØYSUND"
    assert test_org.id == "974760673"
    assert test_org.org_path == "/STAT/912660680/974760673"
    assert test_org.informationmodel_count == 33
    assert test_org.concept_count == 23
    assert test_org.dataset_count == 2
    assert test_org.dataservice_count == 18
